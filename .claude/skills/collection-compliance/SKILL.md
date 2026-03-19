---
name: collection-compliance
description: |
  Check collection.yaml compliance against COLLECTION_SPEC.md. Use when the user asks to:
  - "Validate collection.yaml"
  - "Check collection compliance"
  - "Verify collection.yaml against spec"
  - Before committing collection changes

  Runs structural validation (make validate) and cross-checks: skills on disk vs collection.yaml, orchestration placement, summary_markdown alignment, sample_workflows format (User request + bullets) and consistency with SKILL.md.
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

### Step 4: Resources Cross-Check

For each pack, validate `resources`:

1. **Required fields:** Each resource has `title` and `url` (enforced by `make validate`).
2. **embedded_doc:** When a resource has `embedded_doc`, verify `{pack_dir}/{embedded_doc}` exists on disk. Path is relative to pack root (e.g. `docs/rhel/package-management.md`).
3. **Report:** PASS if all `embedded_doc` paths exist or none present; WARN if any `embedded_doc` points to a missing file.

### Step 4b: Sample Workflows Cross-Check

For each pack, validate `sample_workflows`:

1. **Structure:** Each entry has `name` and `workflow` (enforced by `make validate`).
2. **Placeholder check:** WARN if any entry has placeholder text (e.g. "TODO: Add workflow", "Extract from README Sample Workflows section").
3. **Format check:** Each workflow must start with a user request and use bullet points:
   - **User request:** Workflow text should contain `User: "` or `User:` followed by a quoted request. WARN if missing (e.g. workflow starts with "Use /skill" or numbered steps instead).
   - **Bullet points:** Steps should use `-` bullets. WARN if workflow uses only numbered paragraphs (e.g. "1. Step 2. Step") without bullets, or prose-only format.
   - **Reference:** Per generate-collection skill Step 5b: `User: "..."` first, then `- step` bullets.
4. **Consistency with SKILL.md:**
   - **Skills referenced:** Extract skill names from workflow text (e.g. "remediation skill", "fleet-inventory", "cve-impact"). Each must exist in `contents.skills` or `contents.orchestration_skills`. WARN if workflow references a skill not in the collection.
   - **Orchestration alignment:** For workflows that mention an orchestration skill, read that skill's SKILL.md `## Workflow` section. Verify the workflow steps in the sample_workflow reflect the orchestration steps (e.g. validate → impact → context → playbook → execute). WARN if major steps are missing or order differs significantly.
5. **Content check:** Each orchestration skill should ideally have a corresponding sample_workflow. If pack has orchestration skills but sample_workflows are placeholders or missing orchestration coverage, report WARN: "Consider regenerating sample_workflows from skills (generate-collection skill)."

### Step 5: Report Results

**Output format:**
```
## Collection Compliance Report

### Structural validation
[PASS|FAIL] make validate

### Cross-checks (pack: X)
- [PASS|FAIL] All skills on disk listed in collection.yaml
- [PASS|FAIL] No orchestration skills duplicated in skills
- [PASS|WARN] summary_markdown alignment with SKILL.md
- [PASS|WARN] resources.embedded_doc paths exist
- [PASS|WARN] sample_workflows populated (no placeholders; orchestration skills covered)
- [PASS|WARN] sample_workflows format (User request + bullet points)
- [PASS|WARN] sample_workflows consistency with SKILL.md (skills exist; orchestration steps align)

### Recommendations
- <actionable items>
```

## Dependencies

- `uv` (run `make install` if needed)
- [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) — schema, validation scope, what is not validated
- [scripts/validate_structure.py](../../../scripts/validate_structure.py) — structural validation logic
- [catalog/schema.yaml](../../../catalog/schema.yaml) — schema reference
- [generate-collection SKILL.md](../generate-collection/SKILL.md) — sample_workflows format (Step 5b)

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
| resources.embedded_doc paths exist | This skill | Cross-check |
| sample_workflows populated (no placeholders) | This skill | Cross-check |
| sample_workflows format (User + bullets) | This skill | Cross-check |
| sample_workflows consistency with SKILL.md | This skill | Cross-check |

## Example Usage

**User:** "Check collection compliance for rh-sre"

**Workflow:**
1. Run `make validate` → report pass/fail
2. List `rh-sre/skills/*` and `rh-sre/collection.yaml` contents
3. Compare: any missing? duplicates?
4. Check summary_markdown alignment for all skills
5. Verify resources.embedded_doc paths exist (if any)
6. Check sample_workflows format (User request + bullets) and consistency with SKILL.md
7. Output compliance report with recommendations
