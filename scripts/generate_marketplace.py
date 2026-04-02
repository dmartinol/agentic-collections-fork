#!/usr/bin/env python3
"""
Generate Claude Code and Cursor marketplace.json from collection.yaml definitions.

Discovers all */collection.yaml files and produces:
- .claude-plugin/marketplace.json
- .cursor-plugin/marketplace.json

Each file includes `_generated` metadata ($schema remains first in the Claude file).
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

from generation_notice import attach_json_generation_metadata, write_json, write_json_or_check

REPO_ROOT = Path(__file__).resolve().parent.parent

MARKETPLACE_JSON_SOURCE = (
    "Each plugin entry is generated from the pack's collection.yaml "
    "(see each item's `source` path under the repository root)."
)
MARKETPLACE_OWNER = {
    "name": "Red Hat Ecosystem Engineering",
    "email": "eco-engineering@redhat.com",
}


def discover_collections() -> List[tuple[str, Path, Dict[str, Any]]]:
    """Find all collection.yaml files and load them. Returns (pack_dir, path, data)."""
    collections = []
    for item in sorted(REPO_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        coll_path = item / "collection.yaml"
        if not coll_path.exists():
            continue
        with open(coll_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data:
            collections.append((item.name, coll_path, data))
    return collections


def slugify_category(cat: str) -> str:
    """Convert category to slug for marketplace."""
    return cat.lower().replace(" ", "-").replace("/", "-").replace("&", "and")


def build_claude_marketplace(collections: List[tuple]) -> Dict[str, Any]:
    """Build Claude Code marketplace.json structure."""
    plugins = []
    for pack_dir, _, data in collections:
        plugin_id = data.get("id", pack_dir)
        category = data.get("categories", ["general"])
        cat_slug = slugify_category(category[0]) if category else "general"
        plugins.append({
            "name": plugin_id,
            "description": data.get("description", ""),
            "version": data.get("version", "1.0.0"),
            "author": data.get("author", MARKETPLACE_OWNER),
            "source": f"./{pack_dir}",
            "category": cat_slug,
            "agents": [],
            "skills": "./skills",
        })
    return {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": "redhat-agentic-collections",
        "version": "1.0.0",
        "description": "Validated Agentic Collections from Red Hat Ecosystem Engineering",
        "owner": MARKETPLACE_OWNER,
        "plugins": plugins,
    }


def build_cursor_marketplace(collections: List[tuple]) -> Dict[str, Any]:
    """Build Cursor marketplace.json structure."""
    plugins = []
    for pack_dir, _, data in collections:
        plugin_id = data.get("id", pack_dir)
        category = data.get("categories", ["general"])
        cat_slug = slugify_category(category[0]) if category else "general"
        plugins.append({
            "name": plugin_id,
            "source": pack_dir,
            "description": data.get("description", ""),
            "version": data.get("version", "1.0.0"),
            "author": data.get("author", MARKETPLACE_OWNER),
            "category": cat_slug,
            "skills": "./skills",
        })
    return {
        "name": "redhat-agentic-collections",
        "owner": MARKETPLACE_OWNER,
        "metadata": {
            "description": "Validated Agentic Collections from Red Hat Ecosystem Engineering",
            "version": "1.0.0",
        },
        "plugins": plugins,
    }


def main(check: bool = False) -> int:
    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    claude_data = attach_json_generation_metadata(
        build_claude_marketplace(collections),
        source_of_truth=MARKETPLACE_JSON_SOURCE,
        schema_key_first="$schema",
    )
    cursor_data = attach_json_generation_metadata(
        build_cursor_marketplace(collections),
        source_of_truth=MARKETPLACE_JSON_SOURCE,
    )

    claude_dir = REPO_ROOT / ".claude-plugin"
    cursor_dir = REPO_ROOT / ".cursor-plugin"
    claude_dir.mkdir(exist_ok=True)
    cursor_dir.mkdir(exist_ok=True)

    any_diff = False
    for path, data, label in [
        (claude_dir / "marketplace.json", claude_data, ".claude-plugin/marketplace.json"),
        (cursor_dir / "marketplace.json", cursor_data, ".cursor-plugin/marketplace.json"),
    ]:
        ok = write_json_or_check(path, data, check=check)
        if not ok:
            any_diff = True
        elif not check:
            print(f"Generated {label} ({len(collections)} plugins)")

    if check:
        if any_diff:
            print("Marketplace files are out of sync. Run 'make generate-catalog'.")
            return 1
        print("✓ Marketplace files match sources")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify files match sources without writing")
    args = parser.parse_args()
    sys.exit(main(check=args.check))
