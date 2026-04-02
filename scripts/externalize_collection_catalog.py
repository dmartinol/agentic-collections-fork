#!/usr/bin/env python3
"""
Externalize collection.yaml long markdown fields into <pack>/.catalog/*.md
and replace with *_file references. Idempotent: skips packs already using deploy_and_use_file.

Run from repo root: uv run python scripts/externalize_collection_catalog.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

PACKS = [
    "ocp-admin",
    "rh-ai-engineer",
    "rh-automation",
    "rh-developer",
    "rh-sre",
    "rh-support-engineer",
    "rh-virt",
]

# (inline_body_key, markdown_filename, yaml_file_key)
EXTRACT_SPEC: tuple[tuple[str, str, str], ...] = (
    ("deploy_and_use", "deploy_and_use.md", "deploy_and_use_file"),
    ("documentation_section", "documentation.md", "documentation_section_file"),
    ("mcp_section", "mcp.md", "mcp_section_file"),
    ("security_model", "security.md", "security_model_file"),
)

INLINE_KEYS = {e[0] for e in EXTRACT_SPEC}
EXTRACT_LOOKUP = {body: (fname, fkey) for body, fname, fkey in EXTRACT_SPEC}


def _link_fix(text: str) -> str:
    return text.replace("](../docs/", "](docs/")


def _multiline_str_representer(dumper: yaml.SafeDumper, data: str) -> yaml.Node:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def migrate_pack(pack_dir: str) -> list[str]:
    log: list[str] = []
    path = REPO_ROOT / pack_dir / "collection.yaml"
    if not path.exists():
        return [f"skip {pack_dir}: no collection.yaml"]

    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        return [f"skip {pack_dir}: invalid YAML root"]

    if data.get("deploy_and_use_file"):
        return [f"skip {pack_dir}: already uses .catalog includes"]

    catalog = REPO_ROOT / pack_dir / ".catalog"
    catalog.mkdir(exist_ok=True)

    out_data: dict = {}
    any_extracted = False

    for key, val in data.items():
        if key in INLINE_KEYS:
            fname, fkey = EXTRACT_LOOKUP[key]
            if isinstance(val, str) and val.strip():
                text = _link_fix(val.strip() + "\n")
                (catalog / fname).write_text(text, encoding="utf-8")
                out_data[fkey] = f".catalog/{fname}"
                any_extracted = True
                log.append(f"  wrote {pack_dir}/.catalog/{fname}")
            elif key == "deploy_and_use":
                raise SystemExit(f"{pack_dir}: deploy_and_use must be non-empty")
            # else: optional section omitted — skip key
        else:
            out_data[key] = val

    if not any_extracted:
        return [f"skip {pack_dir}: nothing to extract"]

    MyDumper = yaml.SafeDumper
    MyDumper.add_representer(str, _multiline_str_representer)  # type: ignore[arg-type]

    out_text = yaml.dump(
        out_data,
        Dumper=MyDumper,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )
    path.write_text(out_text, encoding="utf-8")
    log.insert(0, f"migrated {pack_dir}")
    return log


def main() -> None:
    for pack in PACKS:
        for line in migrate_pack(pack):
            print(line)


if __name__ == "__main__":
    main()
