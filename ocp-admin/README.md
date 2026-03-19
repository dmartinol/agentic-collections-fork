# Red Hat OpenShift Administration Agentic Collection

Automation capabilities for OpenShift Container Platform cluster management, workload orchestration, security policies, and operational tasks.

**Persona**: OpenShift Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

Specialized tools for managing OpenShift clusters throughout their lifecycle—**creation**
with the Assisted Installer, **inventory** across self-managed and managed services,
and **multi-cluster health reporting** from kubeconfig contexts.


## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- **Cluster creation and inventory (`cluster-creator`, `cluster-inventory`):**
  - Red Hat account and offline token from https://cloud.redhat.com/openshift/token
  - `export OFFLINE_TOKEN="..."` (never commit the value; plugins use `${OFFLINE_TOKEN}` in `.mcp.json`)
  - Podman (or Docker) to run Assisted Installer / OCM MCP images from `ocp-admin/.mcp.json`
- **Multi-cluster reports (`cluster-report`):**
  - `oc` or compatible CLI and `KUBECONFIG` with contexts for target clusters
  - **openshift-administration** MCP configured per `ocp-admin/.mcp.json`

Copy MCP server definitions from `ocp-admin/.mcp.json` into your Claude Code settings (`/mcp` or `settings.json`). Servers are not auto-installed with the plugin.

### Environment Setup

Configure OpenShift cluster access for reporting:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
oc get nodes
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install ocp-admin
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install ocp-admin
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/ocp-admin ~/.cursor/plugins/ocp-admin
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/ocp-admin ~/.cursor/plugins/ocp-admin
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/ocp-admin ~/.opencode/plugins/ocp-admin
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/ocp-admin ~/.opencode/plugins/ocp-admin
```


## Skills

The pack provides 3 skills for OpenShift cluster lifecycle, inventory, and fleet health.


### cluster-creator - End-to-End Cluster Deployment

Create OpenShift clusters with Red Hat Assisted Installer (SNO or HA) including ISOs, host discovery, networking, and install monitoring.

**Use when:**
- "Create a new OpenShift cluster"
- "Install OpenShift on bare metal or vSphere"
- "Deploy single-node OpenShift"

**What it does:**
- Drives Assisted Installer MCP workflows end-to-end
- Validates hosts, roles, VIPs, and static networking before install
- Requires `OFFLINE_TOKEN` (see Prerequisites)

**Not for:** listing existing clusters (`cluster-inventory`) or post-install day-2 changes without cluster access.



### cluster-inventory - Cluster Discovery and Status

List and inspect clusters across self-managed (OCP, SNO) and managed (ROSA, ARO, OSD) deployments.

**Use when:**
- "List all my clusters"
- "Show cluster status and events"
- "What clusters exist in my account?"

**What it does:**
- Calls Assisted Installer and OCM MCP APIs (read-only)
- Returns identifiers, versions, platforms, and key diagnostics

**Requires:** `OFFLINE_TOKEN` for API access.




### cluster-report - Multi-Cluster Health Report

Generate a consolidated health and resource report across kubeconfig contexts.

**Use when:**
- "Show me a report across all clusters"
- "Compare cluster health"
- "Multi-cluster status overview"

**What it does:**
- Verifies each context targets OpenShift before reporting
- Aggregates nodes, GPUs, namespaces, and pod health

**Requires:** `KUBECONFIG` with appropriate cluster access;
uses **openshift-administration** MCP (see `.mcp.json`).




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| Create, install, or provision an OpenShift cluster (SNO or HA) | cluster-creator | End-to-end Assisted Installer workflow with host discovery, networking, and install monitoring. |
| List clusters, show status, events, or inventory across ROSA/ARO/OSD and self-managed | cluster-inventory | Read-only discovery via Assisted Installer and OCM APIs using OFFLINE_TOKEN. |
| Multi-cluster health report, fleet summary, or compare resource usage across contexts | cluster-report | Uses kubeconfig contexts and openshift-administration MCP for consolidated cluster metrics. |




## Sample Workflows


### Deploy and verify a new cluster

1. Run **cluster-creator** to provision the cluster via Assisted Installer.
2. Run **cluster-inventory** to confirm status and watch events until the cluster is ready.
3. Configure `KUBECONFIG`, then run **cluster-report** for a first health snapshot.



### Fleet health review

1. Run **cluster-inventory** to list managed and self-managed clusters.
2. Align kubeconfig contexts, then run **cluster-report** for resource and pod health across the fleet.



### Multi-Cluster Health Report

User: "Show me a report across all clusters"
- cluster-report skill:
  1. Verifies each kubeconfig context is OpenShift
  2. Collects node resources (CPU, memory, GPUs)
  3. Aggregates namespace counts and pod status
  4. Produces comparison view




## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [OpenShift Container Platform Documentation](https://docs.openshift.com/container-platform/latest/welcome/index.html) - Official OpenShift cluster management and administration docs.


- [OpenShift Multi-Cluster Management](https://docs.openshift.com/container-platform/latest/operators/operator_sdk/osdk-cli-managing-multicluster.html) - Managing multiple OpenShift clusters.

