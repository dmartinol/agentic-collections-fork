#!/usr/bin/env python3
"""
Validate agentic collection structure before documentation generation.

Validates:
- plugin.json, .mcp.json (optional)
- collection.yaml against catalog/schema.yaml
- SKILL.md and agent frontmatter
"""

import json
import sys
from pathlib import Path
from typing import List, Set, Tuple
import yaml
import re

REPO_ROOT = Path(__file__).resolve().parent.parent

# List of agentic collections to validate
PACK_DIRS = ['ocp-admin', 'rh-ai-engineer', 'rh-automation', 'rh-developer', 'rh-sre', 'rh-support-engineer', 'rh-virt']

# Required collection.yaml fields (per catalog/schema.yaml)
REQUIRED_COLLECTION_TOP = ['id', 'name', 'provider', 'version', 'categories', 'personas', 'marketplaces',
                           'description', 'summary', 'contents', 'deploy_and_use', 'sample_workflows', 'resources']
REQUIRED_CONTENTS = ['description', 'skills']
REQUIRED_SKILL_ENTRY = ['name', 'description', 'summary_markdown']
REQUIRED_DECISION_ENTRY = ['user_request', 'skill_to_use', 'reason']
REQUIRED_WORKFLOW_ENTRY = ['name', 'workflow']
REQUIRED_RESOURCE_ENTRY = ['title', 'url']


def validate_collection_yaml(pack_dir: str) -> List[str]:
    """
    Validate collection.yaml against catalog/schema.yaml.

    Args:
        pack_dir: Collection directory name (relative to REPO_ROOT)

    Returns:
        List of error messages (empty if valid)
    """
    errors: List[str] = []
    coll_path = REPO_ROOT / pack_dir / 'collection.yaml'

    if not coll_path.exists():
        errors.append(f"{pack_dir}: collection.yaml not found")
        return errors

    try:
        with open(coll_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"{pack_dir}: Invalid YAML in collection.yaml: {e}")
        return errors

    if not isinstance(data, dict):
        errors.append(f"{pack_dir}: collection.yaml must be a YAML mapping")
        return errors

    # Required top-level fields
    for field in REQUIRED_COLLECTION_TOP:
        if field not in data:
            errors.append(f"{pack_dir}: collection.yaml missing required field '{field}'")
        elif data[field] is None:
            errors.append(f"{pack_dir}: collection.yaml field '{field}' must not be empty")

    # contents
    contents = data.get('contents')
    if contents is not None:
        if not isinstance(contents, dict):
            errors.append(f"{pack_dir}: contents must be a mapping")
        else:
            for field in REQUIRED_CONTENTS:
                if field not in contents:
                    errors.append(f"{pack_dir}: contents missing required field '{field}'")

            # skills
            skills = contents.get('skills')
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

            # orchestration_skills
            orch = contents.get('orchestration_skills')
            if orch is not None and isinstance(orch, list):
                for i, entry in enumerate(orch):
                    if isinstance(entry, dict):
                        for req in REQUIRED_SKILL_ENTRY:
                            if req not in entry:
                                errors.append(f"{pack_dir}: contents.orchestration_skills[{i}] missing '{req}'")

            # skills_decision_guide
            guide = contents.get('skills_decision_guide')
            if guide is not None:
                if not isinstance(guide, list):
                    errors.append(f"{pack_dir}: contents.skills_decision_guide must be a list")
                else:
                    known_skills: Set[str] = set()
                    for s in (contents.get('skills') or []):
                        if isinstance(s, dict) and 'name' in s:
                            known_skills.add(str(s['name']))
                    for o in (contents.get('orchestration_skills') or []):
                        if isinstance(o, dict) and 'name' in o:
                            known_skills.add(str(o['name']))

                    for i, entry in enumerate(guide):
                        if not isinstance(entry, dict):
                            errors.append(f"{pack_dir}: contents.skills_decision_guide[{i}] must be a mapping")
                        else:
                            for req in REQUIRED_DECISION_ENTRY:
                                if req not in entry:
                                    errors.append(f"{pack_dir}: contents.skills_decision_guide[{i}] missing '{req}'")
                            # skill_to_use should reference a known skill
                            if isinstance(entry, dict) and 'skill_to_use' in entry and known_skills:
                                skill_ref = entry.get('skill_to_use')
                                if skill_ref and skill_ref not in known_skills:
                                    errors.append(
                                        f"{pack_dir}: contents.skills_decision_guide[{i}] "
                                        f"skill_to_use '{skill_ref}' not in contents.skills or orchestration_skills"
                                    )

    # sample_workflows
    workflows = data.get('sample_workflows')
    if workflows is not None and isinstance(workflows, list):
        for i, entry in enumerate(workflows):
            if isinstance(entry, dict):
                for req in REQUIRED_WORKFLOW_ENTRY:
                    if req not in entry:
                        errors.append(f"{pack_dir}: sample_workflows[{i}] missing '{req}'")

    # resources
    resources = data.get('resources')
    if resources is not None and isinstance(resources, list):
        for i, entry in enumerate(resources):
            if isinstance(entry, dict):
                for req in REQUIRED_RESOURCE_ENTRY:
                    if req not in entry:
                        errors.append(f"{pack_dir}: resources[{i}] missing '{req}'")

    return errors


def validate_plugin_json(pack_dir: str) -> List[str]:
    """
    Validate plugin.json structure.

    Args:
        pack_dir: Collection directory name

    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    plugin_path = REPO_ROOT / pack_dir / '.claude-plugin' / 'plugin.json'

    if not plugin_path.exists():
        # plugin.json is optional
        return errors

    try:
        with open(plugin_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check required fields
        if 'name' not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'name'")
        if 'version' not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'version'")
        if 'description' not in data:
            errors.append(f"{pack_dir}: plugin.json missing required field 'description'")

    except json.JSONDecodeError as e:
        errors.append(f"{pack_dir}: Invalid JSON in plugin.json: {e}")
    except Exception as e:
        errors.append(f"{pack_dir}: Error reading plugin.json: {e}")

    return errors


def validate_mcp_json(pack_dir: str) -> List[str]:
    """
    Validate .mcp.json structure.

    Args:
        pack_dir: Pack directory name

    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    mcp_path = REPO_ROOT / pack_dir / '.mcp.json'

    if not mcp_path.exists():
        # .mcp.json is optional
        return errors

    try:
        with open(mcp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check for mcpServers key
        if 'mcpServers' not in data:
            errors.append(f"{pack_dir}: .mcp.json missing 'mcpServers' key")
        elif not isinstance(data['mcpServers'], dict):
            errors.append(f"{pack_dir}: .mcp.json 'mcpServers' must be an object")

    except json.JSONDecodeError as e:
        errors.append(f"{pack_dir}: Invalid JSON in .mcp.json: {e}")
    except Exception as e:
        errors.append(f"{pack_dir}: Error reading .mcp.json: {e}")

    return errors


def validate_yaml_frontmatter(file_path: Path) -> Tuple[bool, str]:
    """
    Validate YAML frontmatter in a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return False, "Missing YAML frontmatter (should start with --- and end with ---)"

        frontmatter_text = match.group(1)
        data = yaml.safe_load(frontmatter_text)

        if data is None:
            return False, "Empty YAML frontmatter"

        # Check required fields
        if 'name' not in data:
            return False, "Missing required field 'name' in frontmatter"
        if 'description' not in data:
            return False, "Missing required field 'description' in frontmatter"

        return True, ""

    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_skills(pack_dir: str) -> List[str]:
    """
    Validate skills in a pack.

    Args:
        pack_dir: Pack directory name

    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    skills_dir = REPO_ROOT / pack_dir / 'skills'

    if not skills_dir.exists():
        # Skills directory is optional
        return errors

    # Find all SKILL.md files
    for skill_file in skills_dir.glob('*/SKILL.md'):
        is_valid, error_msg = validate_yaml_frontmatter(skill_file)
        if not is_valid:
            errors.append(f"{skill_file}: {error_msg}")

    return errors


def validate_agents(pack_dir: str) -> List[str]:
    """
    Validate agents in a pack.

    Args:
        pack_dir: Pack directory name

    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    agents_dir = REPO_ROOT / pack_dir / 'agents'

    if not agents_dir.exists():
        # Agents directory is optional
        return errors

    # Find all .md files
    for agent_file in agents_dir.glob('*.md'):
        is_valid, error_msg = validate_yaml_frontmatter(agent_file)
        if not is_valid:
            errors.append(f"{agent_file}: {error_msg}")

    return errors


def validate_pack(pack_dir: str) -> List[str]:
    """
    Validate a single pack.

    Args:
        pack_dir: Pack directory name

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check if pack directory exists
    if not (REPO_ROOT / pack_dir).exists():
        errors.append(f"{pack_dir}: Pack directory does not exist")
        return errors

    # Validate collection.yaml (required)
    errors.extend(validate_collection_yaml(pack_dir))

    # Validate plugin.json
    errors.extend(validate_plugin_json(pack_dir))

    # Validate .mcp.json
    errors.extend(validate_mcp_json(pack_dir))

    # Validate skills
    errors.extend(validate_skills(pack_dir))

    # Validate agents
    errors.extend(validate_agents(pack_dir))

    return errors


def main():
    """
    Main validation function.
    """
    print("🔍 Validating agentic collection structure...")
    print()

    all_errors = []

    for pack_dir in PACK_DIRS:
        print(f"Validating {pack_dir}...", end=' ')
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
    else:
        print("✅ All collections validated successfully")
        print()
        return 0


if __name__ == '__main__':
    sys.exit(main())
