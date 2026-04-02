### Troubleshooting and operations

- **MCP server** — Build and run the OpenShift MCP server image as described in **Quick Start** (this collection’s `deploy_and_use`). Confirm the local image tag matches `.mcp.json`.
- **VM failures** — See [docs/troubleshooting/INDEX.md](docs/troubleshooting/INDEX.md) for conditions, storage, and migration issues.
- **Skills not matching** — Use the **Skills Decision Guide** above or **CLAUDE.md** intent routing.

### Architecture

- Skills under **`skills/`** wrap the **openshift-virtualization** MCP server; they enforce confirmations for destructive actions.
- Namespace-scoped resources: always confirm namespace and VM name before delete, restore, or rebalance.
