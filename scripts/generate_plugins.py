#!/usr/bin/env python3
"""
Generate Claude Code and Cursor plugin.json from collection.yaml definitions.

For each pack with collection.yaml, produces:
- {pack}/.claude-plugin/plugin.json
- {pack}/.cursor-plugin/plugin.json

Each JSON file includes a `_generated` object (source path, do not edit).
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from generation_notice import attach_json_generation_metadata, collection_yaml_source, write_json, write_json_or_check

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


def main(check: bool = False) -> int:
    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    any_diff = False
    for pack_dir, data in collections:
        plugin_data = attach_json_generation_metadata(
            build_plugin_json(data, pack_dir),
            source_of_truth=collection_yaml_source(pack_dir),
        )
        pack_path = REPO_ROOT / pack_dir

        for vendor, subdir in [("claude", ".claude-plugin"), ("cursor", ".cursor-plugin")]:
            vendor_dir = pack_path / subdir
            vendor_dir.mkdir(exist_ok=True)
            out_path = vendor_dir / "plugin.json"
            ok = write_json_or_check(out_path, plugin_data, check=check)
            if not ok:
                any_diff = True
            elif not check:
                print(f"Generated {pack_dir}/{subdir}/plugin.json")

    if check:
        if any_diff:
            print("Plugin files are out of sync. Run 'make generate-catalog'.")
            return 1
        print(f"✓ Plugin files match sources for {len(collections)} packs")
    else:
        print(f"Generated plugin.json for {len(collections)} packs")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify files match sources without writing")
    args = parser.parse_args()
    sys.exit(main(check=args.check))
