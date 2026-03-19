# Collection Specification

Specification for `collection.yaml` — the vendor-agnostic catalog definition for agentic packs. This document describes structure, generation, and how it relates to skills.

## Overview

Each pack has a `collection.yaml` at its root (e.g. `rh-sre/collection.yaml`). It is the **source of truth** for:

- Pack metadata (name, description, personas, marketplaces)
- User-facing skill discovery (skills, orchestration skills, decision guide)
- Deploy and use instructions
- Sample workflows and resources

**Generated artifacts** (do not edit manually):

- `README.md` — Pack README
- `.claude-plugin/plugin.json` — Claude Code plugin metadata
- `.cursor-plugin/plugin.json` — Cursor plugin metadata
- `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json` — Marketplace listings
- `docs/collections/<id>.html` — Collection detail pages

## Schema

Full schema: [catalog/schema.yaml](catalog/schema.yaml)

### Required Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Plugin identifier for install commands (e.g. `claude plugin install <id>`). Defaults to pack folder name. Override for rh-virt: `openshift-virtualization` |
| `name` | string | Display name |
| `provider` | string | Organization (e.g. "Red Hat") |
| `version` | string | Semantic version (e.g. "1.0.0") |
| `categories` | list | Marketplace categories (e.g. ["Site Reliability", "Security"]) |
| `personas` | list | Target personas (e.g. ["Site Reliability Engineer"]) |
| `marketplaces` | list | Supported marketplaces (e.g. ["Claude Code", "Cursor"]) |
| `description` | string | Full description |
| `summary` | string | Short markdown summary |
| `contents` | object | Skills and content (see below) |
| `deploy_and_use` | string | Markdown: prerequisites, env setup, install per marketplace |
| `sample_workflows` | list | `{ name, workflow }` entries |
| `resources` | list | `{ title, description, url }` entries |

### Contents Structure

```yaml
contents:
  description: string   # e.g. "The pack provides 13 skills for common SRE operations..."
  skills:              # Regular skills (exclude orchestration skills)
    - name: string      # Matches skills/<name>/SKILL.md
      description: string
      summary_markdown: string
  orchestration_skills: # Skills that invoke other skills
    - name: string
      description: string
      summary_markdown: string
  skills_decision_guide: # Optional
    - user_request: string
      skill_to_use: string
      reason: string
```

### Skills vs Orchestration Skills

- **skills**: Task executors that use MCP tools directly. Do not invoke other skills.
- **orchestration_skills**: Skills that invoke other skills (e.g. `/remediation` orchestrates `/cve-validation`, `/playbook-generator`, etc.).

Orchestration skills must **not** be duplicated in `skills`. They appear in a separate section in generated README and collection pages (orchestration first, then regular skills).

### summary_markdown

Per-skill user-facing content. Should align with the skill's `description` in SKILL.md.

**Regular skills** — include:
- **Use when:** 3–5 example prompts
- **What it does:** Bullet list of capabilities

**Orchestration skills** — include:
- **Use when:** Example prompts
- **Workflow:** Steps or skills invoked
- **Capabilities:** What the orchestration achieves

See [SKILL_DESIGN_PRINCIPLES.md](SKILL_DESIGN_PRINCIPLES.md) Collection Catalog section for alignment rules.

### skills_decision_guide

Optional array to help users choose the right skill. Rendered as a table in README and collection pages.

- `user_request`: Example user prompt or intent
- `skill_to_use`: Skill name (must exist in `skills` or `orchestration_skills`)
- `reason`: Why this skill fits

## Generation Pipeline

```bash
make generate-catalog   # Generates marketplace, plugins, README
make generate          # generate-catalog + docs (data.json, collection pages)
```

| Script | Produces |
|--------|----------|
| `scripts/generate_marketplace.py` | `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json` |
| `scripts/generate_plugins.py` | `{pack}/.claude-plugin/plugin.json`, `{pack}/.cursor-plugin/plugin.json` |
| `scripts/generate_readme.py` | `{pack}/README.md` (from `catalog/README_TEMPLATE.md.j2`) |
| `scripts/build_website.py` | `docs/data.json`, `docs/collections/{id}.html` |

## Validation

```bash
make validate   # Runs scripts/validate_structure.py
```

Validates `collection.yaml` structure per pack:

| Check | Details |
|-------|---------|
| **Top-level** | Required: `id`, `name`, `provider`, `version`, `categories`, `personas`, `marketplaces`, `description`, `summary`, `contents`, `deploy_and_use`, `sample_workflows`, `resources` |
| **contents.skills** | Each entry has `name`, `description`, `summary_markdown` |
| **contents.orchestration_skills** | Each entry has `name`, `description`, `summary_markdown` |
| **contents.skills_decision_guide** | Each entry has `user_request`, `skill_to_use`, `reason`; `skill_to_use` must reference a skill in `skills` or `orchestration_skills` |
| **sample_workflows** | Each entry has `name`, `workflow` |
| **resources** | Each entry has `title`, `url` |

**Not validated:** Cross-check that all `skills/*/SKILL.md` are listed in `collection.yaml`, or that orchestration skills are not duplicated in `skills`.

## When Adding a Skill

1. Create `skills/<name>/SKILL.md` (see [SKILL_DESIGN_PRINCIPLES.md](SKILL_DESIGN_PRINCIPLES.md))
2. Add to `collection.yaml`:
   - `contents.skills` or `contents.orchestration_skills` with `name`, `description`, `summary_markdown`
   - Optionally add `skills_decision_guide` entry
3. Run `make generate-catalog` to regenerate README and plugins
4. Run `make validate` to confirm structure

## Related Documentation

- [CLAUDE.md](CLAUDE.md) — Pack structure, README skills section, workflow
- [SKILL_DESIGN_PRINCIPLES.md](SKILL_DESIGN_PRINCIPLES.md) — Skill design, Collection Catalog section
- [catalog/schema.yaml](catalog/schema.yaml) — Full schema with field comments
