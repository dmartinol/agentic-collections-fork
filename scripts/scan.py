#!/usr/bin/env python3
"""Run the skill security scan manually for a single collection.

Usage:
  scripts/scan.py <COLLECTION>

Example:
  scripts/scan.py rh-sre

Required environment variables:
  SKILL_SCANNER_LLM_API_KEY

Optional environment variables:
  SKILL_SCANNER_LLM_MODEL
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run cisco-ai-skill-scanner for one collection using the same "
            "flags as .github/workflows/skill-security-scan.yml."
        )
    )
    parser.add_argument(
        "collection",
        help="Collection folder name or path (e.g. rh-sre)",
    )
    parser.add_argument(
        "--output-dir",
        default="security-reports",
        help="Directory for generated reports (default: security-reports)",
    )
    parser.add_argument(
        "--fail-on-severity",
        default="medium",
        choices=["low", "medium", "high", "critical"],
        help="Minimum severity threshold that fails the scan (default: medium)",
    )
    return parser.parse_args()


def _resolve_collection_path(collection_input: str) -> Path:
    candidate = Path(collection_input)
    if candidate.is_absolute():
        collection_path = candidate
    else:
        direct = REPO_ROOT / candidate
        collection_path = direct if direct.exists() else (Path.cwd() / candidate)
    return collection_path.resolve()


def _safe_report_suffix(collection_path: Path) -> str:
    # Keep report names stable and filesystem-safe.
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", collection_path.name)


def main() -> int:
    args = _parse_args()
    collection_path = _resolve_collection_path(args.collection)
    skills_dir = collection_path / "skills"

    if not collection_path.exists():
        print(f"❌ Collection not found: {collection_path}", file=sys.stderr)
        return 2
    if not skills_dir.exists() or not skills_dir.is_dir():
        print(
            f"❌ Expected skills directory not found: {skills_dir}",
            file=sys.stderr,
        )
        return 2

    scanner_bin = shutil.which("skill-scanner")
    if not scanner_bin:
        print(
            "❌ skill-scanner is not installed or not on PATH.\n"
            "Install with:\n"
            "  uv pip install --system 'cisco-ai-skill-scanner[google]'",
            file=sys.stderr,
        )
        return 2

    llm_api_key = os.getenv("SKILL_SCANNER_LLM_API_KEY")
    if not llm_api_key:
        print(
            "❌ SKILL_SCANNER_LLM_API_KEY is not set.\n"
            "Export it before running this script.",
            file=sys.stderr,
        )
        return 2

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = (REPO_ROOT / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    report_name = f"security-report-{_safe_report_suffix(collection_path)}.md"
    report_path = output_dir / report_name

    cmd = [
        scanner_bin,
        "scan-all",
        str(skills_dir),
        "--recursive",
        "--use-behavioral",
        "--use-llm",
        "--check-overlap",
        "--enable-meta",
        "--fail-on-severity",
        args.fail_on_severity,
        "--format",
        "markdown",
        "--detailed",
        "--output",
        str(report_path),
    ]

    print(f"🔍 Scanning collection: {collection_path.name}")
    print(f"📁 Skills directory: {skills_dir}")
    print(f"📝 Report output: {report_path}")
    print(f"⚠️  Fail on severity: {args.fail_on_severity}")
    print("")

    env = os.environ.copy()
    # Pass-through env-based secrets expected by scanner.
    env["SKILL_SCANNER_LLM_API_KEY"] = llm_api_key
    if os.getenv("SKILL_SCANNER_LLM_MODEL"):
        env["SKILL_SCANNER_LLM_MODEL"] = os.environ["SKILL_SCANNER_LLM_MODEL"]

    result = subprocess.run(cmd, env=env, cwd=str(REPO_ROOT), check=False)
    if result.returncode == 0:
        print(f"\n✅ Scan passed. Report: {report_path}")
    else:
        print(
            f"\n❌ Scan failed (exit {result.returncode}). "
            f"See report: {report_path}",
            file=sys.stderr,
        )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
