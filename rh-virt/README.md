# Red Hat OpenShift Virtualization Agentic Collection

Virtual machine management and automation for OpenShift Virtualization and KubeVirt workloads.

**Persona**: Virtualization Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-virt collection provides skills for virtualization tasks.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- OpenShift cluster (>= 4.19) with Virtualization operator installed
- ServiceAccount with appropriate RBAC permissions for VirtualMachine resources
- KUBECONFIG environment variable configured with cluster access

### Environment Setup

Configure OpenShift cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Verify access to the cluster:

```bash
oc get virtualmachines -A
# or
kubectl get vms -A
```

### Building the MCP Server Container Image

The OpenShift MCP server is not published to public registries, so you need to build it locally before using this collection.

**Prerequisites**: Git, Podman (or Docker)

**Build Steps**:

1. Clone the openshift-mcp-server repository:
   ```bash
   git clone https://github.com/openshift/openshift-mcp-server.git
   cd openshift-mcp-server
   ```

2. Build the container image using Podman:
   ```bash
   podman build -t localhost/openshift-mcp-server:latest -f Dockerfile .
   ```
   Or using Docker:
   ```bash
   docker build -t localhost/openshift-mcp-server:latest -f Dockerfile .
   ```

3. Verify the image was built successfully:
   ```bash
   podman images localhost/openshift-mcp-server:latest
   podman tag localhost/openshift-mcp-server:latest quay.io/ecosystem-appeng/openshift-mcp-server:latest
   ```

**Note**: The build process takes several minutes. The final image size is approximately 192 MB.

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install openshift-virtualization
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install openshift-virtualization
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-virt ~/.cursor/plugins/openshift-virtualization
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-virt ~/.cursor/plugins/openshift-virtualization
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-virt ~/.opencode/plugins/openshift-virtualization
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-virt ~/.opencode/plugins/openshift-virtualization
```


## Skills

The pack provides 10 skills for virtual machine management on OpenShift Virtualization.


### vm-clone - VM Cloning

Clone existing virtual machines for testing, scaling, or creating templates.

**Use when:**
- "Clone VM X to Y"
- "Create a copy of VM database-01"
- "Duplicate VM for testing"

**What it does:**
- Clones VM and associated resources
- Supports cross-namespace cloning
- Preserves or customizes configuration



### vm-create - VM Creation

Create new virtual machines in OpenShift Virtualization with automatic instance type resolution and OS selection.

**Use when:**
- "Create a new VM"
- "Deploy a virtual machine with RHEL"
- "Set up a VM in namespace X"

**What it does:**
- Creates VM with appropriate instance type
- Configures OS and resources
- Handles storage and networking



### vm-delete - VM Deletion

Permanently delete virtual machines and their associated resources from OpenShift Virtualization.

**Use when:**
- "Delete VM X"
- "Remove virtual machine Y"
- "Clean up VM and its disks"

**What it does:**
- Deletes VM and associated resources
- Handles DataVolumes and PVCs
- Requires confirmation for destructive action



### vm-inventory - VM Listing and Discovery

List and view virtual machines across namespaces with status, resource usage, and health information.

**Use when:**
- "List all VMs"
- "Show VMs in namespace X"
- "What VMs are running?"

**What it does:**
- Lists VMs across namespaces
- Shows status and resource usage
- Displays health information



### vm-lifecycle-manager - Start, Stop, Restart

Manage virtual machine lifecycle operations including start, stop, and restart.

**Use when:**
- "Start VM X"
- "Stop the virtual machine Y"
- "Restart VM database-01"

**What it does:**
- Starts stopped VMs
- Stops running VMs
- Restarts VMs gracefully



### vm-rebalance - VM Migration

Orchestrate VM migrations across cluster nodes for load balancing, maintenance, and resource optimization.

**Use when:**
- "Move VM database-01 to worker-03"
- "Rebalance VMs to optimize CPU load"
- "Drain node for maintenance"

**What it does:**
- Migrates VMs between nodes
- Supports live migration
- Handles node drain and cordon



### vm-snapshot-create - Snapshot Creation

Create virtual machine snapshots for backup and recovery.

**Use when:**
- "Create a snapshot of VM X"
- "Backup VM before upgrade"
- "Take a snapshot of database-01"

**What it does:**
- Creates VM snapshots
- Validates storage class support
- Manages snapshot resources



### vm-snapshot-delete - Snapshot Deletion

Permanently delete virtual machine snapshots to free storage space.

**Use when:**
- "Delete snapshot X"
- "Remove old VM snapshots"
- "Free space from snapshots"

**What it does:**
- Deletes snapshot resources
- Frees associated storage
- Requires confirmation



### vm-snapshot-list - Snapshot Listing

List virtual machine snapshots with status and metadata.

**Use when:**
- "List snapshots for VM X"
- "Show available backups"
- "What snapshots exist?"

**What it does:**
- Lists snapshots per VM
- Shows status and size
- Displays creation time



### vm-snapshot-restore - Snapshot Restore

Restore virtual machines from existing snapshots.

**Use when:**
- "Restore VM from snapshot"
- "Roll back to snapshot X"
- "Recover VM from backup"

**What it does:**
- Restores VM from snapshot
- Handles disk and configuration
- Preserves or creates new VM





## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "List all VMs" or "Show VMs in namespace X" | vm-inventory | Lists and inspects VM status across namespaces. |
| "Create a new VM" or "Deploy a virtual machine with RHEL" | vm-create | Provisions new VMs with instance type resolution and OS selection. |
| "Start VM X" or "Stop the virtual machine Y" | vm-lifecycle-manager | Manages VM power state (start, stop, restart). |
| "Clone VM X to Y" or "Create a copy of VM database-01" | vm-clone | Clones existing VMs for testing, scaling, or templates. |
| "Move VM database-01 to worker-03" or "Rebalance VMs" | vm-rebalance | Orchestrates live migration across nodes for load balancing. |




## Sample Workflows


### See collection.yaml

Add workflows in collection.yaml.



## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [OpenShift Virtualization Documentation](https://docs.openshift.com/container-platform/latest/virt/about_virt/about-virt.html)


- [KubeVirt User Guide](https://kubevirt.io/user-guide/)


- [OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server)


- [MCP Protocol Specification](https://modelcontextprotocol.io/)


- [Main Repository](https://github.com/RHEcosystemAppEng/agentic-collections)

