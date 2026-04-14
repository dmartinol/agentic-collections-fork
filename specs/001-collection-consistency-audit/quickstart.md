# Quickstart: Collection Consistency Audit

## Purpose

Run metadata and style consistency checks locally, then enforce drift prevention in CI with minimal disruption.

## 1) Run Existing Baseline Checks

From repository root:

```bash
make validate
make validate-skill-design
```

For local incremental work:

```bash
make validate-skill-design-changed
```

## 2) Run Consistency Audit (Planned Command Surface)

Planned repository-native commands:

```bash
# Full matrix + findings for all packs
uv run python scripts/consistency_audit.py --format json --output reports/consistency-audit.json

# Human-readable markdown summary
uv run python scripts/consistency_audit.py --format markdown --output reports/consistency-audit.md

# CI gate mode (fails by policy threshold)
uv run python scripts/consistency_audit.py --ci
```

Expected outputs follow contracts in:

- `specs/001-collection-consistency-audit/contracts/audit-report.schema.json`
- `specs/001-collection-consistency-audit/contracts/ci-violations.schema.json`

## 3) Severity and CI Behavior

- `blocking`: fail CI immediately
- `high`: warning-only in initial rollout; promotable to fail on changed scope
- `medium`: warning-only
- `informational`: report-only

CI policy should be explicit and versioned in repository scripts/workflows.

## 4) Safe Metadata Updates

When updating versions or metadata:

1. Update canonical version in `marketplace/rh-agentic-collection.yml`
2. Reconcile root `README.md` and affected pack `README.md`
3. If optional plugin metadata exists, reconcile plugin version too
4. Re-run local validation and consistency audit before opening PR

## 5) Safe Style/Icon Updates

When updating docs presentation:

1. Prefer tokens in `docs/styles.css` over hardcoded color/size values
2. Keep icon mappings in `docs/icons.json` and pack titles in `docs/plugins.json` synchronized
3. Validate MCP presentation metadata in `docs/mcp.json`
4. Regenerate site data (`make generate`) and verify rendering (`make test`)

## 6) Rh-Support-Engineer Decision Branch

You must choose one explicit policy:

- **Register now**: add marketplace module and enforce full parity checks.
- **Intentionally excluded**: keep unregistered but document explicit exclusion policy and rationale.

If neither path is documented, treat as blocking ambiguity.

## 7) Recommended PR Checklist

- Run: `make validate`
- Run: `make validate-skill-design-changed` (or full)
- Run consistency audit in markdown and JSON modes
- Attach/report severity summary and remediation deltas
- Ensure no new blocking findings before merge
