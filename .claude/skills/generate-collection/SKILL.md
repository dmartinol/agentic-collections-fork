---
name: generate-collection
description: |
  Generate or scaffold collection.yaml from SKILL.md definitions. Use when the user asks to:
  - "Create collection.yaml from skills"
  - "Scaffold collection.yaml for this pack"
  - "Generate collection catalog from SKILL.md files"
  - "Add new skill to collection.yaml"
  - "Regenerate resources" / "Update resources from docs" / "Extract resources from docs"

  Reads skills/<name>/SKILL.md, extracts frontmatter, and produces contents.skills / contents.orchestration_skills entries per COLLECTION_SPEC.md. When regenerating resources, iterates over docs/**/*.md and extracts from frontmatter `sources`.
allowed-tools: Read Glob Grep
---

# Generate Collection from Skills

Scaffold or update `collection.yaml` from existing `skills/*/SKILL.md` definitions. Follows [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) and [catalog/schema.yaml](../../../catalog/schema.yaml).

## When to Use This Skill

Invoke when the user wants to:
- Create a new pack's `collection.yaml` from scratch given existing skills
- Add a newly created skill to an existing `collection.yaml`
- Regenerate `contents.skills` / `contents.orchestration_skills` from SKILL.md files
- Ensure collection.yaml stays in sync with skills on disk

## Workflow

### Step 1: Identify the Pack

**Parameters:**
- `pack_dir`: Pack folder name (e.g. `rh-sre`, `rh-ai-engineer`). Default: ask user or infer from context.

**Action:** Confirm the pack path. Skills live at `{pack_dir}/skills/*/SKILL.md`.

### Step 2: Discover Skills

**Action:** List all skills in the pack:
```bash
# From repo root
ls -1 {pack_dir}/skills/
```

**Document Consultation:** Read [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) Contents Structure and Skills vs Orchestration Skills sections.

### Step 3: Classify Each Skill

For each `skills/<name>/SKILL.md`:

1. **Read** the SKILL.md (frontmatter + first ~50 lines).
2. **Orchestration vs regular:**
   - **Orchestration** if SKILL.md mentions: "orchestrates", "invokes other skills", "invokes the X skill", "delegates to other skills", or lists multiple skills it calls.
   - **Regular** otherwise (uses MCP tools directly, does not invoke other skills).
3. **Extract** from YAML frontmatter:
   - `name`: Must match directory name.
   - `description`: Use as `description` and as base for `summary_markdown`.

### Step 4: Generate Skill Entries

For each skill, produce a YAML entry:

**Regular skill** (`contents.skills`):
```yaml
- name: <skill-name>
  description: <from frontmatter description, first line or short title>
  summary_markdown: |
    **Use when:**
    - <extract from SKILL.md "When to Use" or description>
    - <3-5 example prompts>

    **What it does:**
    - <bullet from SKILL.md capabilities>
```

**Orchestration skill** (`contents.orchestration_skills`):
```yaml
- name: <skill-name>
  description: <from frontmatter>
  summary_markdown: |
    **Use when:**
    - <example prompts>

    **Workflow:** <steps or skills invoked>

    **Capabilities:** <what the orchestration achieves>
```

If SKILL.md has a "When to Use" or "Use when" section, use those prompts. Otherwise derive from the `description` field.

### Step 5: Resources Structure

When creating or updating `resources`, each entry has:

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Display name for the reference |
| `url` | Yes | External URL (e.g. docs.redhat.com, access.redhat.com) |
| `description` | No | Short description shown after the link |
| `embedded_doc` | No | Path to embedded markdown file under the pack (e.g. `docs/rhel/package-management.md`). When present, collection pages show a side link "[embedded doc]" to this file. |

**When regenerating resources** (user asks to "update resources", "regenerate resources", or "extract resources from docs"):

1. **Discover all docs:** List every markdown file under `{pack_dir}/docs/` (e.g. `docs/**/*.md`). Exclude `INDEX.md`, `README.md`, `SOURCES.md` (meta/navigation only).
2. **For each doc with `sources` in frontmatter:** Read the doc's YAML frontmatter. If it has a `sources` array:
   - Use the **first source** (primary reference) for `title` and `url`.
   - Use `sections` from that source (if present) for `description`, or derive from the doc's `title`.
   - Set `embedded_doc` to the doc path relative to pack root (e.g. `docs/ansible/playbook-integration-aap.md`).
3. **Deduplicate by URL:** If multiple docs cite the same `url`, keep one resource per unique URL. For `embedded_doc`, prefer the doc most central to the pack's skills (e.g. cve-remediation-templates over a README).
4. **Add pack-level references:** Include essential external links not derived from docs (e.g. Lightspeed console, MCP server repo) when they support the pack's workflows.

**When only adding a skill** (user did not ask to regenerate resources): Preserve existing `resources`; do not replace them.

### Step 6: Merge or Create collection.yaml

- **If collection.yaml exists:** Preserve top-level metadata (`id`, `name`, `provider`, `version`, `categories`, `personas`, `marketplaces`, `description`, `summary`, `deploy_and_use`, `sample_workflows`, `resources`). Replace only `contents.skills` and `contents.orchestration_skills` with generated entries. Preserve `contents.description`, `contents.skills_decision_guide`, and `resources` unless user asks to regenerate.
- **If collection.yaml does not exist:** Use [catalog/schema.yaml](../../../catalog/schema.yaml) and an existing pack (e.g. `rh-sre`) as template. Generate full structure with placeholder values for metadata; user must fill in `description`, `summary`, `deploy_and_use`, `sample_workflows`, `resources`.

### Step 7: Validate

Run `make validate` to confirm structure. Report any errors and suggest fixes.

## Dependencies

- [COLLECTION_SPEC.md](../../../COLLECTION_SPEC.md) — schema, skills vs orchestration, summary_markdown format
- [catalog/schema.yaml](../../../catalog/schema.yaml) — full schema
- [SKILL_DESIGN_PRINCIPLES.md](../../../SKILL_DESIGN_PRINCIPLES.md) — Collection Catalog section for alignment rules

## Human-in-the-Loop

- **Before overwriting existing collection.yaml:** Show diff or summary of changes. Ask: "Apply these changes to collection.yaml?"
- **New pack:** Confirm placeholder values are acceptable before writing.

## Example Usage

**User:** "Add the new ds-project-setup skill to rh-ai-engineer collection.yaml"

**Workflow:**
1. Read `rh-ai-engineer/skills/ds-project-setup/SKILL.md`
2. Classify as regular (uses MCP tools, no skill invocations)
3. Extract name, description; draft summary_markdown
4. Read existing `rh-ai-engineer/collection.yaml`
5. Append new entry to `contents.skills`
6. Run `make validate`
7. Present diff for user approval

**User:** "Regenerate resources for rh-sre from docs"

**Workflow:**
1. List `rh-sre/docs/**/*.md` (exclude INDEX.md, README.md, SOURCES.md)
2. For each doc with `sources` in frontmatter: extract first source (title, url), add embedded_doc
3. Deduplicate by URL; add pack-level refs (Lightspeed, lightspeed-mcp)
4. Replace `resources` in `rh-sre/collection.yaml`
5. Run `make validate`
