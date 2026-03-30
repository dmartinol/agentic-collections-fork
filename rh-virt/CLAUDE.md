# CLAUDE.md - Red Hat Virtualization Pack

This file provides guidance to Claude Code when working with the **rh-virt** agentic pack.

## Pack Overview

**Red Hat OpenShift Virtualization (KubeVirt) Plugin** for Claude Code - Automate virtual machine lifecycle management, provisioning, and operations on OpenShift clusters.

**Persona**: Virtualization Administrator, OpenShift Administrator
**Marketplaces**: Claude Code, Cursor

## Plugin Installation

Install the rh-virt plugin in Claude Code:

```bash
# Option 1: From GitHub (when published)
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install openshift-virtualization

# Option 2: Local development
claude plugin marketplace add /path/to/agentic-collections
claude plugin install openshift-virtualization

# Verify installation
claude plugin list
# Should show: openshift-virtualization@redhat-agentic-collections
```

**Important**: After installation, you must manually configure the OpenShift MCP server in Claude Code settings. The `.mcp.json` file in this plugin is for **reference only** - MCP servers are NOT automatically installed.

See [README.md](README.md) for complete MCP server setup instructions and building the container image.

## Available Skills

### VM Lifecycle Management

#### 1. vm-inventory

List and view virtual machines across namespaces with status and health information.

**Use when**:
- "List all VMs"
- "Show VMs in namespace [name]"
- "What VMs are running?"
- "Get details of VM [name]"

**Capabilities**: Read-only VM inventory and status reporting

**Color**: cyan (read-only)

#### 2. vm-create

Create new virtual machines with automatic instance type resolution and OS selection.

**Use when**:
- "Create a new VM"
- "Deploy a virtual machine with [OS]"
- "Set up a VM in namespace [name]"
- "Provision a [size] VM"

**Capabilities**: VM provisioning with intelligent defaults for OpenShift Virtualization

**Color**: green (creates resources)

#### 3. vm-lifecycle-manager

Manage VM power state operations (start, stop, restart).

**Use when**:
- "Start VM [name]"
- "Stop the virtual machine [name]"
- "Restart VM [name]"
- "Power on/off VM [name]"

**Capabilities**: Safe VM state transitions with user confirmation

**Color**: blue (modifies state)

#### 4. vm-delete

Permanently delete virtual machines and their associated resources.

**Use when**:
- "Delete VM [name]"
- "Remove virtual machine [name]"
- "Destroy VM [name]"
- "Clean up VM [name]"

**Capabilities**: Permanent VM deletion with confirmation checkpoints

**Color**: red (destructive operation)

#### 5. vm-clone

Clone existing virtual machines for testing, scaling, or creating templates.

**Use when**:
- "Clone VM [source] to [target]"
- "Create a copy of VM [name]"
- "Duplicate VM [name] for testing"
- "Create 3 copies of template-vm"

**Capabilities**: VM cloning with multi-copy support

**Color**: green (creates resources)

#### 6. vm-rebalance

Orchestrate VM migrations across cluster nodes for load balancing and maintenance.

**Use when**:
- "Move VM database-01 to worker-03"
- "Rebalance VMs to optimize CPU load"
- "Drain worker-02 for maintenance"
- "Automatically rebalance the cluster"

**Capabilities**: Manual and automatic VM migration with live/cold migration strategies

**Color**: yellow (affects multiple resources)

### VM Snapshot Management

#### 7. vm-snapshot-create

Create virtual machine snapshots for backup and recovery.

**Use when**:
- "Create a snapshot of VM [name]"
- "Backup VM [name] before upgrade"
- "Take a snapshot of [vm]"

**Capabilities**: VM snapshot creation with storage validation

**Color**: green (creates resources)

#### 8. vm-snapshot-list

List VM snapshots across namespaces with status and recovery information.

**Use when**:
- "List snapshots for VM [name]"
- "Show snapshots in namespace [name]"
- "What snapshots exist for [vm]?"

**Capabilities**: Read-only snapshot inventory

**Color**: cyan (read-only)

#### 9. vm-snapshot-delete

Permanently delete VM snapshots to free storage space.

**Use when**:
- "Delete snapshot [snapshot-name]"
- "Remove old snapshots for VM [name]"
- "Free up snapshot storage"

**Capabilities**: Snapshot deletion with user confirmation

**Color**: red (destructive operation)

#### 10. vm-snapshot-restore

Restore virtual machines from snapshots with strict safety confirmations.

**Use when**:
- "Restore VM [name] from snapshot [snapshot-name]"
- "Roll back VM [name] to snapshot"
- "Recover VM [name] from backup"

**Capabilities**: VM restoration with mandatory VM shutdown and data loss warnings

**Color**: red (destructive operation - overwrites current state)

## MCP Server

This pack uses the **openshift-virtualization** MCP server for all KubeVirt operations.

**Container**: `quay.io/ecosystem-appeng/openshift-mcp-server:latest`
**Auth**: `KUBECONFIG` with cluster access
**Toolset**: `virt` (enabled via `--toolsets virt`)

**Note**: You must build the container image locally before use. See [README.md](README.md) for build instructions.

## Additional Resources

- Complete setup guide: [README.md](README.md)
- Skill quality template: [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
- Main repository: [../README.md](../README.md)
