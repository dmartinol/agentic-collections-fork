#!/usr/bin/env python3
"""
Emit collection.json for each pack: JSON mirror of collection.yaml plus generation metadata.

Resolves optional `{pack}/.catalog/*.md` includes per collection.yaml *_file paths (same as README).

Output: {pack}/collection.json
"""

import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from collection_markdown_includes import apply_markdown_includes
from generation_notice import (
    attach_json_generation_metadata,
    collection_yaml_source,
    write_json,
    yaml_tree_to_json_ready,
)

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
            data = apply_markdown_includes(item.name, data, repo_root=REPO_ROOT)
            result.append((item.name, data))
    return result


def main() -> int:
    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    for pack_dir, data in collections:
        body = yaml_tree_to_json_ready(data)
        out = attach_json_generation_metadata(
            body,
            source_of_truth=collection_yaml_source(pack_dir),
        )
        write_json(REPO_ROOT / pack_dir / "collection.json", out)
        print(f"Generated {pack_dir}/collection.json")

    print(f"Generated collection.json for {len(collections)} packs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
