### Prerequisites

- Claude Code CLI or IDE extension
- **`podman`** (or Docker) for containerized MCP servers where configured in `.mcp.json`
- **`oc`** CLI and **`KUBECONFIG`** for cluster access
- OpenShift cluster with **Red Hat OpenShift AI** operator installed and **KServe** model serving available
- **GPU nodes** for GPU-accelerated inference (see [known-model-profiles.md](../docs/references/known-model-profiles.md) for sizing hints)

**For NVIDIA NIM deployments:** NVIDIA GPU Operator, Node Feature Discovery (NFD), and an **NGC API key** (see **`/nim-setup`** and [NIM on OpenShift AI](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed)).

### Environment Setup

Configure OpenShift AI cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Optional observability MCP URL (when using the remote summarizer pattern):

```bash
export AI_OBSERVABILITY_MCP_URL="https://your-observability-mcp.example"
```

Verify access to OpenShift AI:

```bash
oc get datascienceprojects -A
```

MCP definitions live in **`rh-ai-engineer/.mcp.json`** — copy entries into Claude Code `/mcp` or settings; use **`${...}`** placeholders only for secrets.

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-ai-engineer
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-ai-engineer
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-ai-engineer ~/.cursor/plugins/rh-ai-engineer
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-ai-engineer ~/.cursor/plugins/rh-ai-engineer
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-ai-engineer ~/.opencode/plugins/rh-ai-engineer
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-ai-engineer ~/.opencode/plugins/rh-ai-engineer
```
