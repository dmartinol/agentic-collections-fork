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
