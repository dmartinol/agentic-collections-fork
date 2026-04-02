#!/usr/bin/env python3
"""
Generate README.md from collection.yaml using Jinja2 template.

For each pack with collection.yaml, produces:
- {pack}/README.md (leading HTML comment: source of truth + do not edit)
"""

import sys
from pathlib import Path
from typing import Any, Dict

import yaml
from jinja2 import Environment, FileSystemLoader

from collection_markdown_includes import apply_markdown_includes
from generation_notice import markdown_generation_banner

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "catalog"
TEMPLATE_NAME = "README_TEMPLATE.md.j2"


def load_collection(pack_dir: str) -> Dict[str, Any] | None:
    """Load collection.yaml for a pack."""
    coll_path = REPO_ROOT / pack_dir / "collection.yaml"
    if not coll_path.exists():
        return None
    with open(coll_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def discover_collections() -> list[tuple[str, Dict[str, Any]]]:
    """Find all packs with collection.yaml."""
    result = []
    for item in sorted(REPO_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        data = load_collection(item.name)
        if data:
            data = apply_markdown_includes(item.name, data, repo_root=REPO_ROOT)
            result.append((item.name, data))
    return result


def prepare_template_context(data: Dict[str, Any], pack_dir: str) -> Dict[str, Any]:
    """Prepare context for template. Filter out TODO workflows."""
    ctx = dict(data)
    # Filter sample_workflows with TODO placeholder
    workflows = ctx.get("sample_workflows", [])
    ctx["sample_workflows"] = [w for w in workflows if w.get("name") != "TODO: Add workflow"]
    if not ctx["sample_workflows"] and workflows:
        ctx["sample_workflows"] = [{"name": "See collection.yaml", "workflow": "Add workflows in collection.yaml."}]
    ctx["license"] = data.get("license", "Apache 2.0")
    return ctx


def main() -> int:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template(TEMPLATE_NAME)

    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    for pack_dir, data in collections:
        ctx = prepare_template_context(data, pack_dir)
        out_path = REPO_ROOT / pack_dir / "README.md"
        rendered = template.render(**ctx)
        out_path.write_text(
            markdown_generation_banner(pack_dir) + rendered,
            encoding="utf-8",
        )
        print(f"Generated {pack_dir}/README.md")

    print(f"Generated README for {len(collections)} packs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
