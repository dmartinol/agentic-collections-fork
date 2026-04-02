<!--
  GENERATED FILE — do not edit manually.
  Source of truth: rh-automation/collection.yaml
  Regenerate with: make generate-catalog
-->

# Red Hat Automation Agentic Collection

Ansible Automation Platform governance, execution safety, and forensic troubleshooting tools for Red Hat automation engineers.

**Persona**: Red Hat Automation Governance Architect
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-automation collection provides 11 skills for AAP governance assessment, governed execution, and forensic troubleshooting.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension (or Cursor)
- Red Hat Ansible Automation Platform 2.5+
- AAP API token (Personal Access Token)

### Environment Setup

Configure AAP MCP server and API token:

```bash
export AAP_MCP_SERVER="your-aap-mcp-server.example.com"
export AAP_API_TOKEN="your-personal-access-token"
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-automation
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-automation
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-automation ~/.cursor/plugins/rh-automation
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-automation ~/.cursor/plugins/rh-automation
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-automation ~/.opencode/plugins/rh-automation
```

## Skills

The pack provides 11 skills for AAP governance, execution safety, and forensic troubleshooting, including 3 orchestration skills.


## Orchestration Skills


### governance-assessor - Orchestrates Platform Governance Audit

Orchestrates AAP governance readiness assessments across 7 domains.

**Use when:**
- "Assess my AAP platform's governance readiness"
- "Audit my platform governance"
- "What should I fix before executing jobs?"

**Workflow:**
- Validates MCP connectivity (aap-mcp-validator)
- Runs governance-readiness-assessor (full or scoped)
- Produces execution-summary



### governance-executor - Orchestrates Governed Execution

Orchestrates governed job execution with risk analysis and approval.

**Use when:**
- "Execute the security patch on production urgently"
- Run jobs with check mode and approval

**Workflow:**
- execution-risk-analyzer (inventory risk, secret scanning)
- governed-job-launcher (check mode, approval, phased rollout)



### forensic-troubleshooter - Orchestrates Failure Root Cause Analysis

Orchestrates forensic failure analysis with error classification.

**Use when:**
- "Job #4451 failed. What happened?"
- Troubleshoot job failures

**Workflow:**
- job-failure-analyzer (event extraction, error classification)
- host-fact-inspector (host correlation)
- resolution-advisor (Red Hat doc-backed recommendations)




## Basic Skills


### aap-mcp-validator - Validate AAP MCP Server Connectivity

Validate that required AAP MCP servers are accessible before executing automation skills.

**Use when:**
- Before any skill that requires AAP MCP access
- "Validate AAP MCP", "Check if AAP is configured"
- "Verify AAP connection", "Test AAP MCP servers"

**What it does:**
- Validates one or more of the 6 AAP MCP servers
- Verifies environment variables (AAP_MCP_SERVER, AAP_API_TOKEN)
- Reports connectivity status (PASSED/PARTIAL/FAILED)



### governance-readiness-assessor - 7-Domain Platform Governance Audit

Audit AAP platform across 7 governance domains with Red Hat citations.

**Use when:**
- "Assess my AAP governance", "Is my AAP ready for production?"
- "Check credentials setup", "Audit RBAC", "How are my notifications?"

**What it does:**
- Assesses Workflow Governance, Notification Coverage, RBAC, Credential Security,
  Execution Environments, Workload Isolation, Audit Trail
- Produces PASS/GAP/WARN report with Red Hat documentation citations



### execution-risk-analyzer - Inventory Risk Classification and Secret Scanning

Classify inventory risk and scan extra_vars for secrets before execution.

**Use when:**
- Before executing jobs on production
- "What's the risk of running this on prod?"
- Validate extra_vars for sensitive data

**What it does:**
- Classifies inventory risk (dev/staging/prod)
- Scans extra_vars for potential secrets
- Supports governed execution flow



### governed-job-launcher - Check Mode, Approval, and Phased Rollout

Launch jobs with check mode, approval gates, phased rollout, and rollback.

**Use when:**
- "Execute the security patch on production urgently"
- Run jobs with dry-run before real execution
- Phased rollout across environments

**What it does:**
- Runs check mode before execution
- Requires approval for production targets
- Supports phased rollout and rollback



### job-failure-analyzer - Event Extraction and Error Classification

Extract failure events and classify errors (Platform/Code/Configuration).

**Use when:**
- "Job #4451 failed. What happened?"
- Analyze job failure events
- Classify error type for resolution

**What it does:**
- Extracts failure events from job execution
- Classifies errors using Red Hat taxonomy
- Correlates with host facts for root cause



### host-fact-inspector - Host Fact Correlation with Failures

Correlate host ansible_facts with job failures for root cause analysis.

**Use when:**
- Job failed on specific hosts
- Need host configuration context for failure
- Correlate failures with host facts

**What it does:**
- Retrieves host facts from inventory
- Correlates with failure events
- Supports forensic troubleshooting



### resolution-advisor - Red Hat Doc-Backed Resolution Recommendations

Provide resolution recommendations backed by Red Hat documentation.

**Use when:**
- After error classification in troubleshooting
- Need resolution steps for identified error type
- Advisory guidance (no MCP tools)

**What it does:**
- Maps error types to resolution paths
- Cites Red Hat documentation
- Provides actionable recommendations



### execution-summary - Audit Trail with Doc Consultation Tracking

Generate execution reports for audit and learning purposes.

**Use when:**
- Generate execution summary
- Create audit trail for workflow
- Summarize skills and docs used

**What it does:**
- Analyzes conversation history
- Extracts agents, skills, tools, and docs used
- Provides audit trail for workflows




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "Assess my AAP governance" or "Is my AAP ready for production?" | governance-assessor | Orchestrates full platform governance audit across 7 domains. |
| "Execute the security patch on production" or "Run this job with check mode" | governance-executor | Orchestrates governed execution with risk analysis and approval. |
| "Job #4451 failed. What happened?" or "Troubleshoot this job failure" | forensic-troubleshooter | Orchestrates failure root cause analysis with error classification. |
| "Validate AAP MCP" or "Check AAP connectivity" | aap-mcp-validator | Direct MCP connectivity validation without full assessment. |



## Documentation

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


## MCP Server Integrations

Six HTTP MCP servers (see **`rh-automation/.mcp.json`** and [AAP MCP Server](https://github.com/ansible/aap-mcp-server)):

| Server | Purpose |
|--------|---------|
| **aap-mcp-job-management** | Job templates, launches, events, workflows |
| **aap-mcp-inventory-management** | Inventories, hosts, groups, facts |
| **aap-mcp-configuration** | Notifications, execution environments, platform settings |
| **aap-mcp-security-compliance** | Credentials, credential types, testing |
| **aap-mcp-system-monitoring** | Instance groups, activity stream, mesh, status |
| **aap-mcp-user-management** | Users, teams, organizations, RBAC |

Full governance audits require reachability across **all six**; execution paths may use a subset. Set **`AAP_MCP_SERVER`** and **`AAP_API_TOKEN`** as documented under Quick Start.

## Sample Workflows


### Governance Assessment

User: "Assess my AAP governance - is it ready for production?"
- governance-assessor skill:
  1. Audits AAP platform across 7 governance domains
  2. Produces PASS/GAP/WARN report with Red Hat citations



### Governed Execution

User: "Run this job template with full governance check"
- governance-executor skill:
  1. Performs risk analysis
  2. Runs check mode (dry run) first
  3. Requires approval before production execution
  4. Catches failures in dry run before production



### Forensic Troubleshooting

User: "Job 12345 failed - help me troubleshoot"
- forensic-troubleshooter skill:
  1. Extracts job events and host facts
  2. Classifies errors per taxonomy
  3. Correlates host facts and failures
  4. Provides resolution recommendations




## Security Model

- Never print **`AAP_API_TOKEN`** or raw Bearer material.
- Production job launches require explicit approval paths in **`governed-job-launcher`** / **`governance-executor`**.
- Treat extra_vars and inventory names as sensitive; skills scan for secrets before execution.

## License


[Apache 2.0](LICENSE)


## References


- [Red Hat Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible) - Product overview and capabilities for AAP.


- [AAP 2.5 Security Best Practices](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices) - Credential security, RBAC, separation of duties.


- [AAP 2.6 Troubleshooting Guide (Jobs)](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/troubleshooting_ansible_automation_platform/troubleshoot-jobs) - Job failure analysis, common errors, event interpretation.


- [AAP 2.5 Job Templates and Configuration](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/automation_controller_user_guide/controller-job-templates) - Job execution, check mode, extra_vars, job slicing.


- [AAP 2.6 Troubleshooting Guide](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/troubleshooting_ansible_automation_platform/troubleshoot-jobs) - Error classification taxonomy and resolution paths.


- [AAP MCP Server](https://github.com/ansible/aap-mcp-server) - MCP server for AAP API integration used by this collection.

