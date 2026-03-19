#!/usr/bin/env python3
"""
Validate agentic collection structure before documentation generation.

Validates:
- collection.yaml (required) against catalog expectations
- plugin.json, .mcp.json (optional)
- SKILL.md and agent frontmatter
- CLAUDE.md sections and intent routing when a pack has skills

Skill-level validation (sections, security) is handled by validate-skills.sh and run-skill-linter.sh.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Set, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# List of agentic collections to validate (order matches Makefile verify-generated)
PACK_DIRS = [
    "ocp-admin",
    "rh-ai-engineer",
    "rh-automation",
    "rh-developer",
    "rh-sre",
    "rh-support-engineer",
    "rh-virt",
]

# Required collection.yaml fields (per catalog/schema.yaml)
REQUIRED_COLLECTION_TOP = [
    "id",
    "name",
    "provider",
    "version",
    "categories",
    "personas",
    "marketplaces",
    "description",
    "summary",
    "contents",
    "deploy_and_use",
    "sample_workflows",
    "resources",
]
REQUIRED_CONTENTS = ["description", "skills"]
REQUIRED_SKILL_ENTRY = ["name", "description", "summary_markdown"]
REQUIRED_DECISION_ENTRY = ["user_request", "skill_to_use", "reason"]
REQUIRED_WORKFLOW_ENTRY = ["name", "workflow"]
REQUIRED_RESOURCE_ENTRY = ["title", "url"]

CLAUDE_MD_REQUIRED_SECTIONS = [
    "Skill-First Rule",
    "Intent Routing",
    "MCP Servers",
    "Global Rules",
]


def validate_collection_yaml(pack_dir: str) -> List[str]:
    """
    Validate collection.yaml against catalog/schema.yaml.

    Args:
        pack_dir: Collection directory name (relative to REPO_ROOT)

    Returns:
        List of error messages (empty if valid)
    """
    errors: List[str] = []
    coll_path = REPO_ROOT / pack_dir / "collection.yaml"

    if not coll_path.exists():
        errors.append(f"{pack_dir}: collection.yaml not found")
        return errors

    try:
        with open(coll_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"{pack_dir}: Invalid YAML in collection.yaml: {e}")
        return errors

    if not isinstance(data, dict):
        errors.append(f"{pack_dir}: collection.yaml must be a YAML mapping")
        return errors

    for field in REQUIRED_COLLECTION_TOP:
        if field not in data:
            errors.append(f"{pack_dir}: collection.yaml missing required field '{field}'")
        elif data[field] is None:
            errors.append(f"{pack_dir}: collection.yaml field '{field}' must not be empty")

    contents = data.get("contents")
    if contents is not None:
        if not isinstance(contents, dict):
            errors.append(f"{pack_dir}: contents must be a mapping")
        else:
            for field in REQUIRED_CONTENTS:
                if field not in contents:
                    errors.append(f"{pack_dir}: contents missing required field '{field}'")

            coll_skill_names: Set[str] = set()

            skills = contents.get("skills")
            if skills is not None:
                if not isinstance(skills, list):
                    errors.append(f"{pack_dir}: contents.skills must be a list")
                else:
                    for i, entry in enumerate(skills):
                        if not isinstance(entry, dict):
                            errors.append(f"{pack_dir}: contents.skills[{i}] must be a mapping")
                        else:
                            for req in REQUIRED_SKILL_ENTRY:
                                if req not in entry:
                                    errors.append(f"{pack_dir}: contents.skills[{i}] missing '{req}'")
                            if isinstance(entry.get("name"), str):
                                coll_skill_names.add(entry["name"])

            orch = contents.get("orchestration_skills")
            if orch is not None and isinstance(orch, list):
                for i, entry in enumerate(orch):
                    if isinstance(entry, dict):
                        for req in REQUIRED_SKILL_ENTRY:
                            if req not in entry:
                                errors.append(
                                    f"{pack_dir}: contents.orchestration_skills[{i}] missing '{req}'"
                                )
                        if isinstance(entry.get("name"), str):
                            coll_skill_names.add(entry["name"])

            if isinstance(skills, list):
                skills_dir = REPO_ROOT / pack_dir / "skills"
                if skills_dir.exists():
                    disk_names = {p.parent.name for p in skills_dir.glob("*/SKILL.md")}
                    extra_disk = disk_names - coll_skill_names
                    missing_disk = coll_skill_names - disk_names
                    for name in sorted(extra_disk):
                        errors.append(
                            f"{pack_dir}: skill directory '{name}' exists but is not listed in "
                            f"collection.yaml contents.skills or orchestration_skills"
                        )
                    for name in sorted(missing_disk):
                        errors.append(
                            f"{pack_dir}: collection.yaml lists skill '{name}' but "
                            f"skills/{name}/SKILL.md is missing"
                        )

            guide = contents.get("skills_decision_guide")
            if guide is not None:
                if not isinstance(guide, list):
                    errors.append(f"{pack_dir}: contents.skills_decision_guide must be a list")
                else:
                    known_skills: Set[str] = set()
                    for s in contents.get("skills") or []:
                        if isinstance(s, dict) and "name" in s:
                            known_skills.add(str(s["name"]))
                    for o in contents.get("orchestration_skills") or []:
                        if isinstance(o, dict) and "name" in o:
                            known_skills.add(str(o["name"]))

                    for i, entry in enumerate(guide):
                        if not isinstance(entry, dict):
                            errors.append(
                                f"{pack_dir}: contents.skills_decision_guide[{i}] must be a mapping"
                            )
                        else:
                            for req in REQUIRED_DECISION_ENTRY:
                                if req not in entry:
                                    errors.append(
                                        f"{pack_dir}: contents.skills_decision_guide[{i}] "
                                        f"missing '{req}'"
                                    )
                            if (
                                isinstance(entry, dict)
                                and "skill_to_use" in entry
                                and known_skills
                            ):
                                skill_ref = entry.get("skill_to_use")
                                if skill_ref and skill_ref not in known_skills:
                                    errors.append(
                                        f"{pack_dir}: contents.skills_decision_guide[{i}] "
                                        f"skill_to_use '{skill_ref}' not in contents.skills or "
                                        f"orchestration_skills"
                                    )

    workflows = data.get("sample_workflows")
    if workflows is not None and isinstance(workflows, list):
        for i, entry in enumerate(workflows):
            if isinstance(entry, dict):
                for req in REQUIRED_WORKFLOW_ENTRY:
                    if req not in entry:
                        errors.append(f"{pack_dir}: sample_workflows[{i}] missing '{req}'")
                # Basic content checks for workflow field
                workflow_text = entry.get('workflow')
                if workflow_text is not None and isinstance(workflow_text, str):
                    wf = workflow_text.strip()
                    if not wf:
                        errors.append(f"{pack_dir}: sample_workflows[{i}] workflow is empty")
                    else:
                        # Placeholder check
                        placeholders = [
                            'TODO:', 'todo:', 'Extract from README',
                            'Extract from README Sample Workflows',
                            'placeholder', 'TBD', 'to be added'
                        ]
                        wf_lower = wf.lower()
                        for ph in placeholders:
                            if ph.lower() in wf_lower:
                                errors.append(
                                    f"{pack_dir}: sample_workflows[{i}] contains placeholder '{ph}'"
                                )
                                break
                        # Format: must contain User request (User: or User: ")
                        if 'User:' not in workflow_text and 'user:' not in wf_lower:
                            errors.append(
                                f"{pack_dir}: sample_workflows[{i}] workflow must start with "
                                "User request (e.g. User: \"...\")"
                            )
                        # Format: must contain bullet points (- )
                        if '- ' not in workflow_text:
                            errors.append(
                                f"{pack_dir}: sample_workflows[{i}] workflow must use bullet points (-)"
                            )

    resources = data.get("resources")
    if resources is not None and isinstance(resources, list):
        pack_root = REPO_ROOT / pack_dir
        for i, entry in enumerate(resources):
            if isinstance(entry, dict):
                for req in REQUIRED_RESOURCE_ENTRY:
                    if req not in entry:
                        errors.append(f"{pack_dir}: resources[{i}] missing '{req}'")
                # embedded_doc: path must exist when present
                embedded = entry.get('embedded_doc')
                if embedded and isinstance(embedded, str):
                    doc_path = pack_root / embedded
                    if not doc_path.exists():
                        errors.append(
                            f"{pack_dir}: resources[{i}] embedded_doc '{embedded}' does not exist"
                        )

    return errors


def validate_plugin_json(pack_dir: str) -> List[str]:
    """Validate plugin.json structure."""
    errors: List[str] = []
    plugin_path = REPO_ROOT / pack_dir / ".claude-plugin" / "plugin.json"

    if not plugin_path.exists():
        return errors

    try:
        with open(plugin_path, encoding="utf-8") as f:
            data = json.load(f)

        if "name" not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'name'")
        if "version" not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'version'")
        if "description" not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'description'")

    except json.JSONDecodeError as e:
        errors.append(f"{pack_dir}: Invalid JSON in plugin.json: {e}")
    except OSError as e:
        errors.append(f"{pack_dir}: Error reading plugin.json: {e}")

    return errors


def validate_mcp_json(pack_dir: str) -> List[str]:
    """Validate .mcp.json structure."""
    errors: List[str] = []
    mcp_path = REPO_ROOT / pack_dir / ".mcp.json"

    if not mcp_path.exists():
        return errors

    try:
        with open(mcp_path, encoding="utf-8") as f:
            data = json.load(f)

        if "mcpServers" not in data:
            errors.append(f"{pack_dir}: .mcp.json missing 'mcpServers' key")
        elif not isinstance(data["mcpServers"], dict):
            errors.append(f"{pack_dir}: .mcp.json 'mcpServers' must be an object")

    except json.JSONDecodeError as e:
        errors.append(f"{pack_dir}: Invalid JSON in .mcp.json: {e}")
    except OSError as e:
        errors.append(f"{pack_dir}: Error reading .mcp.json: {e}")

    return errors


def validate_yaml_frontmatter(file_path: Path) -> Tuple[bool, str]:
    """Validate YAML frontmatter in a markdown file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            return False, "Missing YAML frontmatter (should start with --- and end with ---)"

        frontmatter_text = match.group(1)
        data = yaml.safe_load(frontmatter_text)

        if data is None:
            return False, "Empty YAML frontmatter"

        if "name" not in data:
            return False, "Missing required field 'name' in frontmatter"
        if "description" not in data:
            return False, "Missing required field 'description' in frontmatter"

        return True, ""

    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"
    except OSError as e:
        return False, f"Error reading file: {e}"


def validate_skills(pack_dir: str) -> List[str]:
    """Validate skills in a pack."""
    errors: List[str] = []
    skills_dir = REPO_ROOT / pack_dir / "skills"

    if not skills_dir.exists():
        return errors

    for skill_file in skills_dir.glob("*/SKILL.md"):
        is_valid, error_msg = validate_yaml_frontmatter(skill_file)
        if not is_valid:
            errors.append(f"{skill_file.relative_to(REPO_ROOT)}: {error_msg}")

    return errors


def validate_agents(pack_dir: str) -> List[str]:
    """Validate agents in a pack."""
    errors: List[str] = []
    agents_dir = REPO_ROOT / pack_dir / "agents"

    if not agents_dir.exists():
        return errors

    for agent_file in agents_dir.glob("*.md"):
        is_valid, error_msg = validate_yaml_frontmatter(agent_file)
        if not is_valid:
            errors.append(f"{agent_file.relative_to(REPO_ROOT)}: {error_msg}")

    return errors


def validate_claude_md(pack_dir: str) -> List[str]:
    """
    Validate CLAUDE.md presence and structure for packs with skills.
    """
    errors: List[str] = []
    claude_path = REPO_ROOT / pack_dir / "CLAUDE.md"
    skills_dir = REPO_ROOT / pack_dir / "skills"

    has_skills = skills_dir.exists() and any(skills_dir.glob("*/SKILL.md"))

    if not claude_path.exists():
        if has_skills:
            errors.append(f"{pack_dir}: Missing CLAUDE.md (required for packs with skills)")
        return errors

    try:
        with open(claude_path, encoding="utf-8") as f:
            content = f.read()

        headings = re.findall(r"^## (.+)$", content, re.MULTILINE)
        for section in CLAUDE_MD_REQUIRED_SECTIONS:
            if not any(section in h for h in headings):
                errors.append(f"{pack_dir}: CLAUDE.md missing required section '## {section}'")

        if has_skills:
            skill_names = [p.parent.name for p in skills_dir.glob("*/SKILL.md")]
            for skill_name in skill_names:
                if skill_name not in content:
                    errors.append(
                        f"{pack_dir}: CLAUDE.md intent routing missing skill '{skill_name}'"
                    )

    except OSError as e:
        errors.append(f"{pack_dir}: Error reading CLAUDE.md: {e}")

    return errors


def validate_pack(pack_dir: str) -> List[str]:
    """Validate a single pack."""
    errors: List[str] = []

    if not (REPO_ROOT / pack_dir).exists():
        errors.append(f"{pack_dir}: Pack directory does not exist")
        return errors

    errors.extend(validate_collection_yaml(pack_dir))
    errors.extend(validate_plugin_json(pack_dir))
    errors.extend(validate_mcp_json(pack_dir))
    errors.extend(validate_skills(pack_dir))
    errors.extend(validate_agents(pack_dir))
    errors.extend(validate_claude_md(pack_dir))

    return errors


def main() -> int:
    print("🔍 Validating agentic collection structure...")
    print()

    all_errors: List[str] = []

    for pack_dir in PACK_DIRS:
        print(f"Validating {pack_dir}...", end=" ")
        errors = validate_pack(pack_dir)

        if errors:
            print("❌")
            all_errors.extend(errors)
        else:
            print("✓")

    print()

    if all_errors:
        print("❌ Validation failed:")
        print()
        for error in all_errors:
            print(f"  • {error}")
        print()
        return 1

    print("✅ All collections validated successfully")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
