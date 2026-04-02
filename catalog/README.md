# Catalog

Vendor-agnostic catalog infrastructure for agentic collections. Used to generate marketplace entries, plugin metadata, `collection.json`, READMEs, and collection pages from pack `collection.yaml` definitions.

## Contents

| File | Purpose |
|------|---------|
| `schema.yaml` | Collection schema — required fields and structure for `collection.yaml` |
| `README_TEMPLATE.md.j2` | Jinja2 template for pack README generation |
| `collection_page.html.j2` | Template for docs collection detail pages (not used directly; `scripts/generate_collection_pages.py` builds HTML) |
| `marketplace.yaml` | Icon mapping per collection (used by generation scripts) |

## Schema

See [schema.yaml](schema.yaml) for the full schema. Key sections:

- **contents.skills** — Regular skills (exclude orchestration skills)
- **contents.orchestration_skills** — Skills that invoke other skills
- **contents.skills_decision_guide** — Optional user intent → skill mapping

## Generation

Run from repo root:

```bash
make generate-catalog   # marketplace + plugins + collection.json + README
make generate           # generate-catalog + docs (data.json, collection pages)
```

Scripts that consume these files:

- `scripts/generate_marketplace.py` — Reads all `*/collection.yaml`, produces marketplace.json
- `scripts/generate_plugins.py` — Produces plugin.json per pack
- `scripts/generate_collection_json.py` — Produces `collection.json` per pack (JSON mirror + `_generated` metadata)
- `scripts/generate_readme.py` — Renders README_TEMPLATE.md.j2 per pack (HTML comment banner)
- `scripts/collection_markdown_includes.py` — Merges optional `<pack>/.catalog/*.md` referenced by `collection.yaml` `*_file` keys (e.g. `.catalog/mcp.md`)
- `scripts/build_website.py` — Produces docs/data.json and docs/collections/*.html

## Full Specification

See [COLLECTION_SPEC.md](../COLLECTION_SPEC.md) for the complete collection specification, including structure, generation pipeline, and validation.
