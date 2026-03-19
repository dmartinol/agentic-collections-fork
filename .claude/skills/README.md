# Agentic Collections Skills

Project-specific skills for AI assistants (Claude Code, Cursor) working in this repository.

## Location

- **Primary:** `.claude/skills/` — canonical location for Claude Code
- **Cursor:** `.cursor/skills/` — symlinks to `.claude/skills/` for Cursor discovery

## Skills

| Skill | Use when |
|-------|----------|
| **generate-collection** | Create or scaffold `collection.yaml` from `skills/*/SKILL.md` definitions |
| **collection-compliance** | Validate `collection.yaml` against [COLLECTION_SPEC.md](../../COLLECTION_SPEC.md) |
| **compliance-checker** | Validate skills against [SKILL_DESIGN_PRINCIPLES.md](../../SKILL_DESIGN_PRINCIPLES.md) |
| **skill-linter** | Validate skills against agentskills.io specification |

## Adding a New Skill

1. Create `.claude/skills/<name>/SKILL.md`
2. Add symlink: `ln -s ../../.claude/skills/<name> .cursor/skills/<name>`
