# rh-contributor Plugin

**Build high-quality skills for agentic collections** - Guided skill creation with automated validation, quality checks, and marketplace compliance verification.

## Overview

The `rh-contributor` plugin helps community contributors create production-ready skills that meet repository standards and agentskills.io specification requirements. It provides an interactive skill-building workflow with validation, testing, and pull request automation.

## Quick Start

### Installation

```bash
# Add the marketplace (if not already added)
/plugin marketplace add RHEcosystemAppEng/agentic-collections

# Install rh-contributor plugin
/plugin install rh-contributor@redhat-agentic-collections
```

### Usage

```bash
# Start the skill builder
/skill-builder

# Or invoke directly via Skill tool
Skill: "skill-builder"
```

## What You Get

The skill-builder provides:

- **Interactive Guidance**: Question-based workflow for skill definition
- **Smart Pack Detection**: Automatically suggests existing packs or creates new ones
- **Quality Enforcement**: Validates against SKILL_DESIGN_PRINCIPLES.md and agentskills.io spec
- **Automated Validation**: Runs local linter and design validation before commit
- **MCP Configuration**: Guides MCP server selection and .mcp.json setup
- **Git Workflow**: Recommends fork → branch → PR workflow
- **Complete Automation**: Creates directory structure, files, and validates everything

## Skills

| Skill | Description |
|-------|-------------|
| [skill-builder](skills/skill-builder/SKILL.md) | Interactive skill creation with automated quality checks and marketplace compliance |

## Prerequisites

### Required Tools

- **Git**: Version control (fork, branch, commit, PR creation)
- **uv**: Python environment manager (for validation scripts)
  ```bash
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Repository Access

- **Forked Repository**: Fork `RHEcosystemAppEng/agentic-collections` to your GitHub account
- **Cloned Locally**: `git clone https://github.com/YOUR_USERNAME/agentic-collections`

### Knowledge Requirements

- Basic understanding of AI skills and agents
- Familiarity with YAML frontmatter
- Understanding of the technology/platform your skill targets
- Basic Git workflow knowledge

## How It Works

### Workflow Overview

1. **Discovery Phase**
   - Skill-builder asks about skill purpose, target persona, use cases
   - Validates input and checks for existing similar skills
   - Determines whether to use existing pack or create new one

2. **Definition Phase**
   - Defines skill metadata (name, description, color, model)
   - Specifies MCP tools and dependencies
   - Documents workflow steps with precise parameters
   - Adds error handling and common issues

3. **Validation Phase**
   - Runs agentskills.io specification linter
   - Validates against repository design principles
   - Checks for quality issues and missing sections
   - Provides detailed feedback for fixes

4. **Git Workflow Phase** (User Confirmation Required)
   - Creates branch (if needed)
   - Stages skill files
   - Creates commit with co-authorship
   - Optional: Creates pull request to upstream

### Quality Standards

All skills created by skill-builder comply with:

**Tier 1 - agentskills.io Specification** (Automated):
- Valid YAML frontmatter with required fields
- Proper naming conventions (kebab-case)
- Section structure and ordering
- Parameter documentation
- **Validation**: `./scripts/run-skill-linter.sh`

**Tier 2 - Repository Design Principles** (Automated):
- Document consultation transparency (DP1)
- Precise parameter specification (DP2)
- Concise descriptions <500 tokens (DP3)
- Dependencies declaration (DP4)
- Human-in-the-loop for critical ops (DP5)
- Mandatory sections in correct order (DP6)
- MCP server verification (DP7)
- Pack-level CLAUDE.md routing (DP11)
- **Validation**: `make validate-skill-design-changed`

See [SKILL_DESIGN_PRINCIPLES.md](../SKILL_DESIGN_PRINCIPLES.md) for complete details.

## Example Usage

### Creating a Skill for Existing Pack

```
User: "I want to create a skill for rh-virt that creates VM backups"

Claude: [Invokes /skill-builder]

Skill-Builder:
1. What does the skill do? (1 sentence)
   > "Create virtual machine backups using snapshots"

2. What persona uses this skill?
   > "Virtualization administrators"

3. Which pack should this skill belong to?
   Detected existing pack: rh-virt (virtualization administrators)
   Use rh-virt? (yes/no)
   > yes

4. What MCP tools does it need?
   > vm-snapshot-create

5. Is this a destructive operation?
   > no, creates backup

[... continues with questions ...]

[Generates skill, validates, runs tests, creates commit]

✅ Skill created: rh-virt/skills/vm-backup-create/SKILL.md
✅ Validation passed: agentskills.io spec compliant
✅ Design principles: all checks passed
✅ Ready for pull request

Next: Create PR to RHEcosystemAppEng/agentic-collections from your fork
```

### Creating a New Pack

```
User: "I need a skill for security auditing"

Skill-Builder:
Detected persona: Security Engineer
No existing pack found for this persona.

Create new pack "rh-security"? (yes/no)
> yes

[Creates complete pack structure with CLAUDE.md, README.md, etc.]
[Guides through skill creation]
[Validates everything]

✅ Pack created: rh-security/
✅ Skill created: rh-security/skills/security-audit/SKILL.md
✅ Validation passed
```

## Git Workflow

The skill-builder recommends this workflow:

### 1. Fork Repository

```bash
# On GitHub: Fork RHEcosystemAppEng/agentic-collections to your account
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agentic-collections
cd agentic-collections
```

### 2. Create Branch

```bash
# Skill-builder can do this automatically, or manually:
git checkout -b feat/my-new-skill
```

### 3. Create Skill

```bash
# In Claude Code
/skill-builder
# Follow interactive prompts
```

### 4. Review and Commit

```bash
# Skill-builder stages and commits automatically with user confirmation
# Or manually:
git add <pack>/skills/<skill-name>/
git commit -m "feat: add <skill-name> skill to <pack>"
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feat/my-new-skill

# Create PR from your fork to upstream
# Skill-builder can guide this, or use GitHub UI
```

## Validation Commands

Run these manually if needed:

```bash
# Validate skill structure
./scripts/run-skill-linter.sh rh-virt/skills/my-skill/

# Validate design principles (changed skills only)
make validate-skill-design-changed

# Validate entire pack
make validate-skill-design PACK=rh-virt

# Validate repository structure
make validate
```

## Common Issues

### Issue 1: "Skill name already exists"

**Cause**: Another skill in the pack has the same name

**Solution**:
1. Choose a different, more specific name
2. Check existing skills: `ls <pack>/skills/`
3. Consider if your skill overlaps with existing one

### Issue 2: "Validation failed - description too long"

**Cause**: Frontmatter description exceeds 500 tokens

**Solution**:
1. Shorten the description to focus on "Use when" examples
2. Move detailed information to skill body
3. Run word count: `head -n 20 SKILL.md | wc -w`

### Issue 3: "MCP server not configured"

**Cause**: Pack's .mcp.json doesn't include required MCP server

**Solution**:
1. Skill-builder will guide you to add it
2. Or manually add to `<pack>/.mcp.json`
3. Use `${ENV_VAR}` format for credentials

## Tips for Success

### Before Starting

- **Read existing skills** in the target pack for patterns
- **Review SKILL_DESIGN_PRINCIPLES.md** for quality requirements
- **Check MCP servers** available in pack's .mcp.json
- **Understand your use case** - be specific about what the skill does

### During Creation

- **Be concise** - skill-builder will prompt for specific answers
- **Provide examples** - real user phrases for "Use when" section
- **Think about errors** - common issues users will encounter
- **Validate early** - skill-builder validates progressively

### After Creation

- **Test locally** - try invoking your skill in Claude Code
- **Read the generated skill** - ensure it matches your intent
- **Check validation output** - fix any warnings
- **Follow PR template** - describe your skill's value

## Contributing to skill-builder

Found a bug or have a feature request for skill-builder itself?

1. Open an issue: [agentic-collections/issues](https://github.com/RHEcosystemAppEng/agentic-collections/issues)
2. Describe the problem or enhancement
3. Tag with `skill-builder` label

## Resources

- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Complete contribution guide
- **[SKILL_DESIGN_PRINCIPLES.md](../SKILL_DESIGN_PRINCIPLES.md)**: Quality standards and rationale
- **[agentskills.io](https://agentskills.io)**: Specification documentation
- **[Documentation Site](https://rhecosystemappeng.github.io/agentic-collections)**: Browse all collections and skills

## License

Apache License 2.0 - see [LICENSE](../LICENSE)
