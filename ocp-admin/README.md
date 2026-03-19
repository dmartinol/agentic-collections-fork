# Red Hat OpenShift Administration Agentic Collection

Automation capabilities for OpenShift Container Platform cluster management, workload orchestration, security policies, and operational tasks.

**Persona**: OpenShift Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The ocp-admin collection provides skills for openshift tasks.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- OpenShift cluster with cluster-admin or appropriate RBAC
- `oc` CLI and `KUBECONFIG` configured for cluster access

### Environment Setup

Configure OpenShift cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Verify access:

```bash
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

The pack provides 1 skill for OpenShift cluster management.



### cluster-report - Multi-Cluster Health Report

Generate a consolidated health report across multiple OpenShift clusters.

**Use when:**
- "Show me a report across all clusters"
- "Compare cluster health"
- "Multi-cluster status overview"
- "How are my clusters doing?"

**What it does:**
- Verifies each kubeconfig context is a genuine OpenShift cluster
- Collects node resources (CPU, memory, GPUs)
- Reports namespace counts and pod status
- Provides single comparison view across clusters




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "Show me a report across all clusters" or "Compare cluster health" | cluster-report | Generates consolidated health report across multiple OpenShift clusters. |
| "Multi-cluster status overview" or "How are my clusters doing?" | cluster-report | Single skill for cluster health; verifies kubeconfig contexts and reports node resources, pods, namespaces. |




## Sample Workflows


### See collection.yaml

Add workflows in collection.yaml.



## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Main Repository](https://github.com/RHEcosystemAppEng/agentic-collections) - agentic-collections

