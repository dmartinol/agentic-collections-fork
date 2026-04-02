#!/usr/bin/env python3
"""
Shared generation notices for catalog outputs (README, JSON artifacts).

All paths in notices are relative to the repository root.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping


def collection_yaml_source(pack_dir: str) -> str:
    """Relative POSIX path from repo root to the pack's collection.yaml."""
    return f"{pack_dir}/collection.yaml"


def markdown_generation_banner(pack_dir: str) -> str:
    """HTML comment block placed at the top of generated Markdown files."""
    rel = collection_yaml_source(pack_dir)
    return (
        "<!--\n"
        "  GENERATED FILE — do not edit manually.\n"
        f"  Source of truth: {rel}\n"
        "  Regenerate with: make generate-catalog\n"
        "-->\n\n"
    )


def json_generation_block(*, source_of_truth: str) -> dict[str, Any]:
    return {
        "notice": "This file is generated. Do not edit manually.",
        "source_of_truth": source_of_truth,
        "regenerate": "make generate-catalog",
    }


def attach_json_generation_metadata(
    payload: Mapping[str, Any],
    *,
    source_of_truth: str,
    schema_key_first: str | None = None,
) -> dict[str, Any]:
    """
    Return a new dict with _generated metadata and payload contents.

    If schema_key_first is set and that key exists in payload, it is written first
    (then _generated, then the rest) so $schema can stay at the top for consumers
    that expect it first.
    """
    gen = json_generation_block(source_of_truth=source_of_truth)
    pl = dict(payload)
    pl.pop("_generated", None)

    if schema_key_first and schema_key_first in pl:
        first_val = pl.pop(schema_key_first)
        out: dict[str, Any] = {schema_key_first: first_val, "_generated": gen}
        out.update(pl)
        return out

    return {"_generated": gen, **pl}


def yaml_tree_to_json_ready(obj: Any) -> Any:
    """Convert structures from yaml.safe_load into json-serializable values."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): yaml_tree_to_json_ready(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [yaml_tree_to_json_ready(v) for v in obj]
    if isinstance(obj, tuple):
        return [yaml_tree_to_json_ready(v) for v in obj]
    return str(obj)


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    """Write UTF-8 JSON with trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(data), f, indent=2, ensure_ascii=False)
        f.write("\n")
