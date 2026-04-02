#!/usr/bin/env python3
"""
Resolve optional Markdown includes declared in collection.yaml.

YAML keys (optional, per pack):
  deploy_and_use_file
  documentation_section_file
  mcp_section_file
  security_model_file

Values are paths relative to the pack directory, e.g. `.catalog/mcp.md` (must live under
`<pack>/.catalog/`). No path traversal.

Resolved content is written to the matching field without the _file suffix;
*_file keys are removed from the returned dict.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

# Prose fragments for catalog generation live here (per pack).
CATALOG_FRAGMENTS_PREFIX = ".catalog"

# (yaml_file_key, merged_body_key)
FILE_BODY_FIELDS: tuple[tuple[str, str], ...] = (
    ("deploy_and_use_file", "deploy_and_use"),
    ("documentation_section_file", "documentation_section"),
    ("mcp_section_file", "mcp_section"),
    ("security_model_file", "security_model"),
)


def _normalize_include_path(raw: str) -> str:
    p = raw.strip().replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _normalize_catalog_markdown_links(text: str) -> str:
    """
    Fragments may use ../docs/ so links resolve when editing under .catalog/.
    Generated README and JSON use pack-root-relative docs/... paths.
    """
    return text.replace("](../docs/", "](docs/")


def _safe_pack_markdown_path(pack_root: Path, relative: str) -> Path:
    rel = _normalize_include_path(relative)
    if not rel or rel.startswith("/") or ".." in Path(rel).parts:
        raise ValueError(f"Invalid include path: {relative!r}")
    if not (
        rel == CATALOG_FRAGMENTS_PREFIX
        or rel.startswith(f"{CATALOG_FRAGMENTS_PREFIX}/")
    ):
        raise ValueError(
            f"Include path must be under '.catalog/' (e.g. '.catalog/mcp.md'), got {relative!r}"
        )
    root = pack_root.resolve()
    path = (pack_root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError as err:
        raise ValueError(f"Path escapes pack directory: {relative!r}") from err
    return path


def apply_markdown_includes(
    pack_dir: str,
    data: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """
    Return a copy of data with Markdown fragments loaded from paths under the pack.
    *_file keys are stripped from the result after resolution.
    """
    root = repo_root or REPO_ROOT
    out = dict(data)
    pack_root = root / pack_dir

    for file_key, body_key in FILE_BODY_FIELDS:
        rel = out.pop(file_key, None)
        if rel is None:
            continue
        if not isinstance(rel, str) or not rel.strip():
            raise ValueError(f"{pack_dir}: {file_key} must be a non-empty string")
        path = _safe_pack_markdown_path(pack_root, rel)
        if not path.is_file():
            raise FileNotFoundError(f"{pack_dir}: {file_key} -> {path} (missing)")
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError(f"{pack_dir}: {file_key} -> {path} is empty")
        out[body_key] = _normalize_catalog_markdown_links(text)

    return out


def validate_markdown_include_refs(pack_dir: str, data: dict[str, Any]) -> list[str]:
    """
    Return error strings for invalid or missing include references (for validate_structure).
    """
    errors: list[str] = []
    root = REPO_ROOT
    pack_root = root / pack_dir

    for file_key, _body_key in FILE_BODY_FIELDS:
        rel = data.get(file_key)
        if rel is None:
            continue
        if not isinstance(rel, str) or not rel.strip():
            errors.append(f"{pack_dir}: {file_key} must be a non-empty string when set")
            continue
        try:
            path = _safe_pack_markdown_path(pack_root, rel)
        except ValueError as e:
            errors.append(f"{pack_dir}: {file_key}: {e}")
            continue
        if not path.is_file():
            errors.append(f"{pack_dir}: {file_key} points to missing file: {path.relative_to(root)}")
        elif path.stat().st_size == 0:
            errors.append(f"{pack_dir}: {file_key} points to empty file: {path.relative_to(root)}")

    return errors


def deploy_and_use_satisfied(pack_dir: str, data: dict[str, Any]) -> bool:
    """True if deploy_and_use is non-empty after YAML load, or deploy_and_use_file resolves to a non-empty file."""
    v = data.get("deploy_and_use")
    if isinstance(v, str) and v.strip():
        return True
    fk = data.get("deploy_and_use_file")
    if not (isinstance(fk, str) and fk.strip()):
        return False
    try:
        path = _safe_pack_markdown_path(REPO_ROOT / pack_dir, fk)
    except ValueError:
        return False
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False
