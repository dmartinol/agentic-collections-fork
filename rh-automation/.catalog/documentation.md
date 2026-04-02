### What this collection adds over raw MCP access

Raw MCP access can list templates, launch jobs, and read events. This pack adds:

1. **Knowledge** — In-repo docs distilled from Red Hat sources (cited at runtime). Start with embedded references: [docs/aap/governance-readiness.md](docs/aap/governance-readiness.md), [docs/aap/execution-governance.md](docs/aap/execution-governance.md), [docs/aap/job-troubleshooting.md](docs/aap/job-troubleshooting.md), [docs/references/error-classification.md](docs/references/error-classification.md).
2. **Judgment** — Skills interpret MCP data through governance and risk patterns (secret scans, inventory classification, error taxonomy).
3. **Workflow** — Orchestration skills (**`governance-assessor`**, **`governance-executor`**, **`forensic-troubleshooter`**) chain sub-skills with human-in-the-loop gates.

### Three primary use cases

**1. Governance assessment** — *"Assess my AAP platform's governance readiness."*  
Entry: **`governance-assessor`** → audits seven domains across all MCP endpoints; see **governance-readiness** doc above.

**2. Governed execution** — *"Execute the security patch on production urgently."*  
Entry: **`governance-executor`** → risk analysis, check mode, approval before production.

**3. Forensic troubleshooting** — *"Job #4451 failed. What happened?"*  
Entry: **`forensic-troubleshooter`** → events, host facts, doc-backed resolutions (**job-troubleshooting**, **error-classification**).

### Skills × MCP coverage (summary)

| Skill | Typical MCP scope |
|-------|-------------------|
| `governance-assessor` | All 6 servers (orchestrated audit) |
| `governance-executor` | job-management, inventory-management |
| `forensic-troubleshooter` | job-management, inventory-management |
| `aap-mcp-validator` | All 6 (connectivity) |
| `governance-readiness-assessor` | All 6 |
| `execution-risk-analyzer`, `governed-job-launcher` | job-management (+ inventory as needed) |
| `job-failure-analyzer` | job-management |
| `host-fact-inspector` | inventory-management |
| `resolution-advisor`, `execution-summary` | Advisory / reporting (consult docs) |
