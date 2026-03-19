# Red Hat SRE Agentic Collection

Site reliability engineering tools and automation for managing Red Hat platforms and infrastructure.

**Persona**: Site Reliability Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-sre collection provides skills for site reliability tasks.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- Podman or Docker installed
- Red Hat Lightspeed service account ([setup guide](https://console.redhat.com/))

### Environment Setup

Configure Red Hat Lightspeed credentials:

```bash
export LIGHTSPEED_CLIENT_ID="your-service-account-client-id"
export LIGHTSPEED_CLIENT_SECRET="your-service-account-client-secret"
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-sre
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-sre
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-sre ~/.cursor/plugins/rh-sre
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-sre ~/.cursor/plugins/rh-sre
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-sre ~/.opencode/plugins/rh-sre
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-sre ~/.opencode/plugins/rh-sre
```


## Skills

The pack provides 13 skills for common SRE operations, including one orchestration skill for end-to-end remediation.


### fleet-inventory - System Discovery and Fleet Management

Query and display Red Hat Lightspeed managed system inventory.

**Use when:**
- Show the managed fleet
- List all RHEL 8 systems
- What systems are registered in Lightspeed?

**What it does:**
- Retrieves all registered systems
- Groups by RHEL version and environment
- Shows system health and check-in status
- Identifies stale systems



### cve-impact - CVE Discovery and Risk Assessment

Analyze CVE impact across the fleet without immediate remediation.

**Use when:**
- What are the most critical vulnerabilities?
- Show CVEs affecting my systems
- List high-severity CVEs

**What it does:**
- Lists CVEs by severity (Critical/Important)
- Sorts by CVSS score
- Shows affected system counts
- Provides priority recommendations



### cve-validation - CVE Verification

Validate CVE existence and remediation availability.

**Use when:**
- Is CVE-2024-1234 valid?
- Does CVE-X have a remediation?
- What's the CVSS score for CVE-Y?

**What it does:**
- Verifies CVE in Red Hat database
- Checks remediation availability
- Returns CVE metadata and severity



### system-context - System Information Gathering

Collect detailed system information from Red Hat Lightspeed.

**Use when:**
- What systems are affected by CVE-X?
- Show me details for server-01
- Get system profile for these hosts

**What it does:**
- Retrieves system details
- Shows installed packages
- Displays configuration data
- Maps CVE-to-system relationships



### playbook-generator - Ansible Playbook Creation

Generate Ansible remediation playbooks following Red Hat best practices.

**Use when:**
- Create a remediation playbook for CVE-X
- Generate Ansible playbook to patch CVE-Y

**What it does:**
- Calls Red Hat Lightspeed remediation API
- Generates production-ready Ansible playbooks
- Includes error handling and rollback steps
- Follows Red Hat standards



### playbook-executor - AAP Playbook Execution

Execute Ansible playbooks via AAP with dry-run, real-time monitoring, and reporting.

**Use when:**
- Execute this remediation playbook
- Run the playbook and monitor status

**What it does:**
- Launches jobs via AAP MCP (job_templates_launch_retrieve)
- Performs Git Flow (commit, push, sync) when playbook path differs from template
- Monitors job status (PENDING → RUNNING → COMPLETED)
- Reports execution results

**Note:** Requires AAP MCP servers configured and job templates created (use job-template-creator skill).



### remediation-verifier - Remediation Verification

Verify that CVE remediations were successfully applied.

**Use when:**
- Check if CVE-X was patched on server-01
- Verify remediation status

**What it does:**
- Queries current CVE status
- Verifies package updates
- Confirms remediation success



### mcp-lightspeed-validator - Lightspeed MCP Server Validation

Validate Red Hat Lightspeed MCP server configuration and connectivity.

**Use when:**
- Validate Lightspeed MCP
- Check if Lightspeed is configured
- Verify Lightspeed connection
- Other skills need to verify lightspeed-mcp availability

**What it does:**
- Checks MCP server configuration in .mcp.json
- Verifies environment variables (CLIENT_ID, CLIENT_SECRET)
- Tests server connectivity and tool availability
- Reports validation status (PASSED/PARTIAL/FAILED)



### mcp-aap-validator - AAP MCP Server Validation

Validate AAP MCP server configuration and connectivity.

**Use when:**
- Validate AAP MCP
- Check if AAP is configured
- Verify AAP connection
- Other skills need to verify AAP MCP server availability

**What it does:**
- Checks both AAP MCP servers (job-management, inventory-management)
- Verifies environment variables (AAP_MCP_SERVER, AAP_API_TOKEN)
- Tests server connectivity and authentication
- Reports validation status (PASSED/PARTIAL/FAILED)



### execution-summary - Workflow Execution Report

Generate concise execution reports for audit and learning purposes.

**Use when:**
- Generate execution summary
- Create execution report
- Summarize what was used
- Show execution summary

**What it does:**
- Analyzes conversation history
- Extracts agents, skills, tools, and docs used
- Formats in machine-readable format
- Provides audit trail for workflows



### job-template-creator - AAP Job Template Creation

Create AAP job templates for executing Ansible playbooks through Ansible Automation Platform.

**Use when:**
- Create a job template for this playbook
- Set up a template to run remediation playbooks
- Configure AAP to execute this playbook

**What it does:**
- Lists available projects and inventories
- Provides instructions for template creation (Web UI or API)
- Verifies template creation
- Prepares for AAP-based playbook execution



### job-template-remediation-validator - AAP Job Template Remediation Validation

Verify an AAP job template meets requirements for executing CVE remediation playbooks.

**Use when:**
- Does this job template support remediation playbooks?
- Validate job template X for CVE remediation
- Check if template is ready for playbook-executor

**What it does:**
- Validates required fields (inventory, project, playbook, credentials, privilege escalation)
- Checks recommended options (ask variables/limit on launch)
- Verifies project and inventory exist
- Reports PASSED / PASSED WITH WARNINGS / FAILED




## Orchestration Skill


### remediation - End-to-End CVE Remediation

The remediation skill orchestrates 6 specialized skills to provide complete CVE remediation workflows.

**Use when:**
- Remediate CVE-2024-1234 on system abc-123
- Create and execute a remediation playbook for CVE-X
- Patch these 5 CVEs on all production servers

**Workflow:**
0. Validate MCP (mcp-lightspeed-validator, mcp-aap-validator)
1. Impact (cve-impact skill, if needed)
2. Validate CVE (cve-validation skill)
3. Gather Context (system-context skill)
4. Generate Playbook (playbook-generator skill)
5. Execute (playbook-executor skill, with user confirmation)
6. Verify (remediation-verifier skill)

**Capabilities:**
- Single CVE on single system
- Batch remediation (multiple CVEs, multiple systems)
- Cross-environment patching (dev → staging → prod)
- Automated job tracking and reporting
- Partial failure handling





## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "Show the managed fleet" or "List RHEL systems" | fleet-inventory | Discovers and displays Lightspeed-managed system inventory. |
| "What are the most critical CVEs?" or "Show CVEs affecting my systems" | cve-impact | Analyzes CVE impact across the fleet without immediate remediation. |
| "Remediate CVE-2024-1234 on system abc-123" or "Patch these CVEs on production" | remediation | Orchestrates full workflow (validate → context → playbook → execute → verify). |
| "Create a remediation playbook for CVE-X" (no execution yet) | playbook-generator | Generates Ansible playbook only; use playbook-executor to run it. |
| "Does this job template support remediation playbooks?" | job-template-remediation-validator | Validates AAP job template for CVE remediation requirements. |




## Sample Workflows


### See collection.yaml

Add workflows in collection.yaml.



## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Red Hat Lightspeed](https://console.redhat.com/insights)


- [lightspeed-mcp GitHub](https://github.com/redhat/lightspeed-mcp)


- [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible)


- [AAP REST API Documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/)


- [Claude Code Documentation](https://docs.anthropic.com/claude-code)


- [MCP Protocol Specification](https://modelcontextprotocol.io/)


- [Main Repository](https://github.com/RHEcosystemAppEng/agentic-collections)

