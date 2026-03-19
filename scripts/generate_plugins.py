#!/usr/bin/env python3
"""
Generate Claude Code and Cursor plugin.json from collection.yaml definitions.

For each pack with collection.yaml, produces:
- {pack}/.claude-plugin/plugin.json
- {pack}/.cursor-plugin/plugin.json
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


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
            result.append((item.name, data))
    return result


def build_plugin_json(data: Dict[str, Any], pack_dir: str) -> Dict[str, Any]:
    """Build plugin.json structure from collection data."""
    plugin_id = data.get("id", pack_dir)
    return {
        "name": plugin_id,
        "version": data.get("version", "1.0.0"),
        "description": data.get("description", ""),
        "author": data.get("author", {"name": "Red Hat Ecosystem Engineering", "email": "eco-engineering@redhat.com"}),
        "homepage": data.get("homepage", "https://github.com/RHEcosystemAppEng/agentic-collections"),
        "repository": data.get("repository", "https://github.com/RHEcosystemAppEng/agentic-collections"),
        "license": data.get("license", "Apache-2.0"),
        "keywords": data.get("keywords", []),
    }


def main() -> int:
    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    for pack_dir, data in collections:
        plugin_data = build_plugin_json(data, pack_dir)
        pack_path = REPO_ROOT / pack_dir

        for vendor, subdir in [("claude", ".claude-plugin"), ("cursor", ".cursor-plugin")]:
            vendor_dir = pack_path / subdir
            vendor_dir.mkdir(exist_ok=True)
            out_path = vendor_dir / "plugin.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(plugin_data, f, indent=2)
            print(f"Generated {pack_dir}/{subdir}/plugin.json")

    print(f"Generated plugin.json for {len(collections)} packs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
