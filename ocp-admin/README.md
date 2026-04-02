<!--
  GENERATED FILE — do not edit manually.
  Source of truth: ocp-admin/collection.yaml
  Regenerate with: make generate-catalog
-->

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
claude plugin install openshift-administration
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install openshift-administration
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
- Verifies each kubeconfig context targets OpenShift before reporting
- Collects node resources (CPU, memory, GPUs)
- Reports namespace counts and pod health
- Provides a single comparison view across clusters

**Requires:** `KUBECONFIG` with appropriate cluster access;
uses **openshift-administration** MCP (see `.mcp.json`).




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| Create, install, or provision an OpenShift cluster (SNO or HA) | cluster-creator | End-to-end Assisted Installer workflow with host discovery, networking, and install monitoring. |
| List clusters, show status, events, or inventory across ROSA/ARO/OSD and self-managed | cluster-inventory | Read-only discovery via Assisted Installer and OCM APIs using OFFLINE_TOKEN. |
| Multi-cluster health report, fleet summary, or compare resource usage across contexts | cluster-report | Uses kubeconfig contexts and openshift-administration MCP for consolidated cluster metrics. |



## Documentation

### Multi-cluster authentication

For consolidated **cluster-report** across many contexts, set up kubeconfig and RBAC using the pack guide: [docs/multi-cluster-auth.md](docs/multi-cluster-auth.md).

### Further documentation

- **[Documentation index](docs/INDEX.md)** — navigation for networking, host requirements, troubleshooting, and static networking.
- **Troubleshooting** — see [docs/troubleshooting.md](docs/troubleshooting.md) for Assisted Installer and cluster-specific issues.

### Configuration notes

- Ensure `OFFLINE_TOKEN` is exported before Assisted Installer or OCM MCP calls.
- Point `KUBECONFIG` at a merged kubeconfig when reporting across fleets; verify with `oc config get-contexts`.



## MCP Server Integrations

Skills wrap MCP servers defined in **`.mcp.json`** (copy entries into Claude Code `/mcp` or your settings file). Typical layout:

- **openshift-self-managed** — Assisted Installer API for **cluster-creator** / parts of **cluster-inventory** (self-managed OCP, SNO). Requires `OFFLINE_TOKEN`.
- **openshift-ocm-managed** — OpenShift Cluster Manager API for ROSA, ARO, OSD in **cluster-inventory**. Requires `OFFLINE_TOKEN`.
- **openshift-administration** — Kubernetes/OpenShift access for **cluster-report** (node and workload metrics). Requires `KUBECONFIG`.

Images and commands reference `ocp-admin/.mcp.json`; use Podman or Docker as documented there.


## Sample Workflows


### Deploy and verify a new cluster

User: "Provision a new OpenShift cluster and verify it is healthy"
- **cluster-creator** provisions the cluster via Assisted Installer
- **cluster-inventory** confirms status and watches events until the cluster is ready
- Configure `KUBECONFIG`, then **cluster-report** captures a first health snapshot



### Fleet health review

User: "How is my fleet doing across kubeconfig contexts?"
- **cluster-inventory** lists managed and self-managed clusters
- Align kubeconfig contexts, then **cluster-report** reports resource and pod health across the fleet



### Multi-Cluster Health Report

User: "Show me a report across all clusters"
- **cluster-report** verifies each kubeconfig context is OpenShift
- **cluster-report** collects node resources (CPU, memory, GPUs)
- **cluster-report** aggregates namespace counts and pod status
- **cluster-report** produces a comparison view




## Security Model

- **Secrets:** Never print `OFFLINE_TOKEN`, kubeconfig contents, pull secrets, or install keys. Confirm only that required environment variables are set.
- **Human approval:** **cluster-creator** waits for explicit confirmation before VIP assignment, host roles, static networking, and install triggers.
- **Read vs write:** **cluster-inventory** is discovery-focused; **cluster-report** should use least-privilege kubeconfig where possible.


## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [OpenShift Container Platform Documentation](https://docs.openshift.com/container-platform/latest/welcome/index.html) - Official OpenShift cluster management and administration docs.


- [OpenShift Multi-Cluster Management](https://docs.openshift.com/container-platform/latest/operators/operator_sdk/osdk-cli-managing-multicluster.html) - Managing multiple OpenShift clusters.

