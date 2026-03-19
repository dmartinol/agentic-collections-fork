---
name: collection-compliance
description: |
  Check collection.yaml compliance against COLLECTION_SPEC.md. Use when the user asks to:
  - "Validate collection.yaml"
  - "Check collection compliance"
  - "Verify collection.yaml against spec"
  - Before committing collection changes

  Runs structural validation (make validate) and cross-checks: skills on disk vs collection.yaml, orchestration placement, summary_markdown alignment.
allowed-tools: Read Glob Grep
---

# Collection Compliance Checker

Validate `collection.yaml` against [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) and repository principles. Complements `make validate` (structural checks) with cross-checks and alignment checks.

## When to Use This Skill

Invoke when the user wants to:
- Validate collection.yaml before committing or opening a PR
- Check that all skills in `skills/` are listed in collection.yaml
- Verify orchestration skills are not duplicated in `skills`
- Assess summary_markdown alignment with SKILL.md

## Workflow

### Step 1: Run Structural Validation

**Action:** From repo root:
```bash
make validate
```

**Document Consultation:** Read [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) Validation section for what is checked.

**Report:** If `make validate` fails, list errors and suggest fixes per the schema. Stop here until structural issues are resolved.

### Step 2: Cross-Check Skills on Disk vs collection.yaml

For each pack in `PACK_DIRS` (see `scripts/validate_structure.py`):

1. **List skills on disk:** `{pack}/skills/*/` → skill names (directory names).
2. **List skills in collection.yaml:** `contents.skills` + `contents.orchestration_skills` → skill names.
3. **Compare:**
   - **Missing in collection:** Skills in `skills/` but not in collection.yaml. Report as: "Skill X exists in skills/ but is not in collection.yaml."
   - **Orphan in collection:** Skills in collection.yaml but no `skills/<name>/SKILL.md`. Report as: "Skill X is in collection.yaml but skills/X/SKILL.md does not exist."
   - **Orchestration duplicate:** Any skill in `contents.orchestration_skills` that also appears in `contents.skills`. Report as: "Skill X is in both orchestration_skills and skills; remove from skills."

### Step 3: summary_markdown Alignment (Required)

For each skill in collection.yaml, compare `summary_markdown` with SKILL.md:

- **Use when:** Does summary_markdown include 3–5 example prompts? Does SKILL.md "When to Use" or description align?
- **What it does / Workflow:** Does summary_markdown reflect capabilities from SKILL.md?

Report as PASS (aligned) or WARN (misalignment found). Per COLLECTION_SPEC, summary_markdown "should align" with SKILL.md. This check is mandatory—always perform it for every skill in the pack.

### Step 4: Report Results

**Output format:**
```
## Collection Compliance Report

### Structural validation
[PASS|FAIL] make validate

### Cross-checks (pack: X)
- [PASS|FAIL] All skills on disk listed in collection.yaml
- [PASS|FAIL] No orchestration skills duplicated in skills
- [PASS|WARN] summary_markdown alignment with SKILL.md

### Recommendations
- <actionable items>
```

## Dependencies

- `uv` (run `make install` if needed)
- [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) — schema, validation scope, what is not validated
- [scripts/validate_structure.py](../../../scripts/validate_structure.py) — structural validation logic
- [catalog/schema.yaml](../../../catalog/schema.yaml) — schema reference

## What Is Checked vs Not Checked

| Check | Source | Status |
|-------|--------|--------|
| Required top-level fields | validate_structure.py | Automated |
| contents.skills/orchestration_skills structure | validate_structure.py | Automated |
| skills_decision_guide references | validate_structure.py | Automated |
| sample_workflows, resources structure | validate_structure.py | Automated |
| All skills/* in collection.yaml | This skill | Cross-check |
| Orchestration not in skills | This skill | Cross-check |
| summary_markdown aligns with SKILL.md | This skill | Required cross-check |

## Example Usage

**User:** "Check collection compliance for rh-sre"

**Workflow:**
1. Run `make validate` → report pass/fail
2. List `rh-sre/skills/*` and `rh-sre/collection.yaml` contents
3. Compare: any missing? duplicates?
4. Check summary_markdown alignment for all skills
5. Output compliance report with recommendations
