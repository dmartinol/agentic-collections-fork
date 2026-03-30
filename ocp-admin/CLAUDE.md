# CLAUDE.md - OpenShift Administration Pack

This file provides guidance to Claude Code when working with the **ocp-admin** agentic pack.

## Pack Overview

**OpenShift Administration Plugin** for Claude Code - Automate OpenShift cluster lifecycle management, multi-cluster operations, and administration tasks.

**Persona**: OpenShift Administrator
**Marketplaces**: Claude Code, Cursor

## Plugin Installation

Install the ocp-admin plugin in Claude Code:

```bash
# Option 1: From GitHub (when published)
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install ocp-admin

# Option 2: Local development
claude plugin marketplace add /path/to/agentic-collections
claude plugin install ocp-admin

# Verify installation
claude plugin list
# Should show: ocp-admin@redhat-agentic-collections
```

**Important**: After installation, you must manually configure MCP servers in Claude Code settings. The `.mcp.json` file in this plugin is for **reference only** - MCP servers are NOT automatically installed.

See [README.md](README.md) for complete MCP server setup instructions.

## Available Skills

### 1. cluster-creator

End-to-end OpenShift cluster deployment using Red Hat Assisted Installer.

**Use when**:
- "Create a new OpenShift cluster"
- "Install OpenShift on my servers"
- "Set up a single-node cluster for edge deployment"
- "Deploy a production HA cluster"

**Capabilities**:
- SNO (Single-Node OpenShift) and HA (multi-node) clusters
- Platforms: baremetal, vsphere, oci, nutanix
- VIP configuration for HA clusters (API + Ingress)
- Static networking with NMState
- ISO generation and host discovery
- 18-step guided workflow with user confirmations

**MCP Server**: `openshift-self-managed`

### 2. cluster-inventory

List and inspect all OpenShift cluster types with status information.

**Use when**:
- "List my OpenShift clusters"
- "Show cluster status"
- "Get details about cluster [name]"
- "What clusters are installing?"

**Capabilities**:
- Lists self-managed clusters (OCP, SNO) via Assisted Installer API
- Lists managed service clusters (ROSA, ARO, OSD) via OCM API
- Unified view across all cluster types
- Installation progress tracking
- Read-only operations (safe for monitoring)

**MCP Servers**: `openshift-self-managed`, `openshift-ocm-managed`

### 3. cluster-report

Generate consolidated health reports across multiple OpenShift clusters.

**Use when**:
- "Generate a health report for all my clusters"
- "Show resource usage across clusters"
- "List pods with issues in the fleet"
- "Multi-cluster status overview"

**Capabilities**:
- Aggregates metrics from multiple clusters (CPU, memory, GPU)
- Identifies failed pods and attention items
- Per-cluster and fleet-wide summaries
- Supports 10–100+ clusters via service account tokens
- Verifies OpenShift clusters (skips non-OpenShift contexts)

**MCP Server**: `openshift-administration`

## Additional Resources

- Complete setup guide: [README.md](README.md)
- Documentation (17+ guides): [docs/INDEX.md](docs/INDEX.md)
- Main repository: [../README.md](../README.md)
