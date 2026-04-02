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
