#!/usr/bin/env python3
"""
Bootstrap collection.yaml for all packs from existing plugin.json, README, and SKILL.md.

One-time migration script. Produces first draft; manual refinement expected for:
- deploy_and_use (structure per agent)
- sample_workflows
- resources
- contents.skills.summary_markdown (extract "Use when" / "What it does" from skills)
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Packs to process
PACK_DIRS = [
    "rh-sre",
    "rh-developer",
    "ocp-admin",
    "rh-virt",
    "rh-ai-engineer",
    "rh-support-engineer",
]

# Plugin ID override when folder name differs from marketplace install ID
ID_OVERRIDES = {
    "rh-virt": "openshift-virtualization",
}

# Category mapping from marketplace category to schema categories
CATEGORY_MAP = {
    "sre": ["Site Reliability", "Security"],
    "developer": ["Development", "DevOps"],
    "virtualization": ["Virtualization", "OpenShift"],
    "openshift": ["OpenShift", "Administration"],
    "ai-engineering": ["AI/ML", "OpenShift"],
}

# Default categories when not in marketplace
DEFAULT_CATEGORIES = {"Site Reliability", "Development"}


def parse_yaml_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            return {}
        return yaml.safe_load(match.group(1)) or {}
    except Exception as e:
        print(f"Warning: Failed to parse frontmatter from {file_path}: {e}")
        return {}


def load_plugin_json(pack_dir: str, repo_root: Path) -> Dict[str, Any]:
    """Load plugin.json from pack directory."""
    plugin_path = repo_root / pack_dir / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        return {"name": pack_dir, "version": "0.0.0", "description": ""}
    with open(plugin_path, encoding="utf-8") as f:
        return json.load(f)


def get_display_name(pack_dir: str, plugin: Dict[str, Any], repo_root: Path) -> str:
    """Get display name from plugin.json or pack directory name."""
    return plugin.get("name", pack_dir)


def get_marketplace_entry(pack_dir: str, repo_root: Path) -> Optional[Dict[str, Any]]:
    """Get marketplace entry for pack (by source path)."""
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_path.exists():
        return None
    with open(marketplace_path, encoding="utf-8") as f:
        data = json.load(f)
    for plugin in data.get("plugins", []):
        source = plugin.get("source", "")
        if source == f"./{pack_dir}":
            return plugin
    return None


def parse_skills(pack_dir: str, repo_root: Path) -> List[Dict[str, Any]]:
    """Parse skills from skills/*/SKILL.md."""
    skills_dir = repo_root / pack_dir / "skills"
    if not skills_dir.exists():
        return []
    skills = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        frontmatter = parse_yaml_frontmatter(skill_file)
        name = frontmatter.get("name", skill_file.parent.name)
        description = frontmatter.get("description", "")
        if isinstance(description, str):
            description = " ".join(description.split())[:200]
        # Build minimal summary_markdown from description (placeholder for manual refinement)
        summary = f"See SKILL.md for full details.\n\n**Description:** {description}"
        skills.append({
            "name": name,
            "description": description[:100] + ("..." if len(description) > 100 else ""),
            "summary_markdown": summary,
        })
    return skills


def extract_readme_section(content: str, section: str) -> Optional[str]:
    """Extract markdown content between ## Section and next ##."""
    pattern = rf"^##\s+{re.escape(section)}\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else None


def extract_resources_from_readme(content: str) -> List[Dict[str, str]]:
    """Extract resource links from References section."""
    refs = extract_readme_section(content, "References")
    if not refs:
        return []
    resources = []
    for line in refs.split("\n"):
        # Match markdown links: - [Title](url) or - [Title](url) - desc
        match = re.match(r"^-\s+\[([^\]]+)\]\(([^)]+)\)(?:\s*-\s*(.+))?$", line.strip())
        if match:
            title, url, desc = match.groups()
            resources.append({"title": title, "url": url, "description": desc or ""})
    return resources


def build_collection(pack_dir: str, repo_root: Path) -> Dict[str, Any]:
    """Build collection.yaml structure from existing sources."""
    plugin = load_plugin_json(pack_dir, repo_root)
    marketplace = get_marketplace_entry(pack_dir, repo_root)
    skills = parse_skills(pack_dir, repo_root)

    collection_id = ID_OVERRIDES.get(pack_dir, pack_dir)
    display_name = get_display_name(pack_dir, plugin, repo_root)

    # Categories from marketplace or default
    if marketplace and "category" in marketplace:
        cat = marketplace["category"]
        categories = CATEGORY_MAP.get(cat, [cat.replace("-", " ").title()])
    else:
        categories = list(DEFAULT_CATEGORIES)

    # Persona from first category or pack name
    personas = [categories[0] + " Engineer"] if categories else ["Platform Engineer"]

    readme_path = repo_root / pack_dir / "README.md"
    deploy_and_use = "TODO: Extract from README Quick Start section."
    resources = []
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")
        quick_start = extract_readme_section(readme_content, "Quick Start")
        if quick_start:
            deploy_and_use = quick_start
        resources = extract_resources_from_readme(readme_content)

    return {
        "id": collection_id,
        "name": display_name,
        "provider": "Red Hat",
        "version": plugin.get("version", "1.0.0"),
        "categories": categories,
        "personas": personas,
        "marketplaces": ["Claude Code", "Cursor"],
        "support_level": "Unknown",
        "description": plugin.get("description", f"{display_name} agentic collection."),
        "summary": f"The {pack_dir} collection provides skills for {categories[0].lower()} tasks.",
        "contents": {
            "description": f"The pack provides {len(skills)} skills. TODO: Refine from README.",
            "skills": skills,
        },
        "deploy_and_use": deploy_and_use,
        "sample_workflows": [
            {"name": "TODO: Add workflow", "workflow": "Extract from README Sample Workflows section."}
        ],
        "resources": resources or [
            {"title": "Main Repository", "description": "agentic-collections", "url": "https://github.com/RHEcosystemAppEng/agentic-collections"}
        ],
        "legal_resources": {
            "license_agreement_url": "https://www.redhat.com/en/about/agreements",
            "privacy_policy_url": "https://www.redhat.com/en/about/privacy-policy",
        },
        "author": plugin.get("author", {"name": "Red Hat Ecosystem Engineering", "email": "eco-engineering@redhat.com"}),
        "homepage": plugin.get("homepage", "https://github.com/RHEcosystemAppEng/agentic-collections"),
        "repository": plugin.get("repository", "https://github.com/RHEcosystemAppEng/agentic-collections"),
        "license": plugin.get("license", "Apache-2.0"),
        "keywords": plugin.get("keywords", []),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    for pack_dir in PACK_DIRS:
        pack_path = repo_root / pack_dir
        if not pack_path.is_dir():
            print(f"Skipping {pack_dir}: not a directory")
            continue
        collection = build_collection(pack_dir, repo_root)
        out_path = pack_path / "collection.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(collection, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Generated {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
