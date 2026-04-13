# Collection catalog specification

This repository uses a **pack-local collection catalog**: curated metadata and summaries live under **`<pack>/.catalog/`** (YAML as the source of record, JSON as a deterministic mirror for consumers that prefer it). **Golden sources** are pack `SKILL.md` files, `README.md`, `CLAUDE.md`, and [`marketplace/rh-agentic-collection.yml`](marketplace/rh-agentic-collection.yml). Catalog files **describe** the collection for tooling and documentation; they are **authored** primarily via the [**create-collection**](.claude/skills/create-collection/SKILL.md) skill (assistant + maintainer + PR review) and must not overwrite READMEs or marketplace YAML.

**Machine validation:** [`catalog/schema.yaml`](catalog/schema.yaml) (JSON Schema expressed in YAML) and [`scripts/validate_collection_compliance.py`](scripts/validate_collection_compliance.py). **Pack list:** union of Lola marketplace `modules[].path` and keys of [`docs/plugins.json`](docs/plugins.json), limited to directories that exist on disk — see [`scripts/pack_registry.py`](scripts/pack_registry.py).

## Layout

| Path | Purpose |
|------|---------|
| `<pack>/.catalog/collection.yaml` | Canonical catalog document (YAML) |
| `<pack>/.catalog/collection.json` | Deterministic JSON mirror of YAML (regenerate with `make catalog-mirror-json`; CI fails on drift) |
| `<pack>/.catalog/*.md` | Optional prose fragments, **siblings of** `collection.yaml`. Reference them with **`#<filename>.md`** (quoted in YAML). If inline text in `collection.yaml` for a monitored field exceeds **`CATALOG_INLINE_CHAR_LIMIT`** (500 Unicode code points; see `scripts/collection_validate_lib.py`), move it here and point with the matching `*_file` key or `deploy_and_use` file-ref flavor. |

### External references (`#…md` and `*_file`)

- **Path rule:** refs are **siblings of** `collection.yaml` inside **`<pack>/.catalog/`**. Write **`#install.md`**, not `#.catalog/install.md` (omit the `.catalog/` segment in the string).
- **Monitored inline length:** for **`summary`**, **`documentation_section`**, **`mcp_section`**, and **`security_model`**, if the value is an inline string longer than **500 Unicode code points**, move the prose to a fragment file and set the matching `*_file` key to **`#<filename>.md`**. For **`deploy_and_use`**, the same limit applies when it is **inline** markdown (not a one-line ref).
- **`deploy_and_use` (two flavors):** (1) **Inline** — markdown in YAML, ≤ **500** code points unless you externalize. (2) **File ref** — one line only: **`#<file>.md`** (same directory as `collection.yaml`). CI resolves the file under **`<pack>/.catalog/`**.
- **`*_file` values:** must start with **`#`** (e.g. `#documentation_section.md`). Legacy `#.catalog/…` is accepted and normalized.

**Plugin / install IDs:** default `id` equals the pack directory name. Overrides: **`rh-virt`** → `openshift-virtualization`; **`ocp-admin`** → `openshift-administration`.

## Source precedence (pack-local)

When multiple sources could supply the same logical field:

1. **`skills/*/SKILL.md`** (per-skill `name`, `description`, body for `summary_markdown` hints)
2. **`<pack>/README.md`**
3. **`<pack>/CLAUDE.md`** (intent routing for decision-guide hints, personas)

**Lola marketplace:** the module whose `path` equals `<pack>` supplies `version`, module `name`, module `description`, and `tags` for listing-oriented fields. **Never** write back to marketplace YAML from automation or the create-collection workflow.

## Provenance banners

| Artifact | Banner |
|----------|--------|
| `collection.yaml` | Leading `#` comment block: must mention **create-collection** workflow and **golden sources** (SKILL, README, CLAUDE, marketplace). |
| `.catalog/*.md` fragments | Leading HTML `<!-- ... -->` with the same intent. |
| `collection.json` | **No** embedded banner; **CI** regenerates from YAML and fails if the committed file differs. |

## Orchestration vs regular skills

**Primary:** maintainer / assistant judgment while following **create-collection**. **Optional:** `metadata.collection.role: orchestration` in `SKILL.md` frontmatter for clearer compliance checks — not required on every skill.

## Completeness and CI

All **required** schema fields must be present on merge to `main` (no empty placeholders, no `TODO:` / `TBD` in `sample_workflows.workflow`). CI runs **`make validate`** (includes structure + **collection compliance**).

## Related

- [`SKILL_DESIGN_PRINCIPLES.md`](SKILL_DESIGN_PRINCIPLES.md) — skill content (Tier 2)
- [`.claude/skills/collection-compliance/SKILL.md`](.claude/skills/collection-compliance/SKILL.md) — validation workflow
