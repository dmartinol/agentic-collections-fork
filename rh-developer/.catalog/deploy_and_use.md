### Prerequisites

- Claude Code CLI or IDE extension
- **OpenShift** cluster with build/deploy capabilities (for OpenShift skills)
- **`oc`** CLI and **`KUBECONFIG`** for cluster-scoped skills
- **Podman** installed locally (S2I builds, **podman** MCP, local image workflows)
- **Git**; **GitHub personal access token** when analyzing private GitHub repos via **`github`** MCP
- **Helm** CLI (for **`/helm-deploy`**)
- **Optional — Red Hat Insights / Lightspeed** (`LIGHTSPEED_CLIENT_ID`, `LIGHTSPEED_CLIENT_SECRET`) for **`/debug-rhel`** and **`/rhel-deploy`** advisor data

**Supported languages** (detection / S2I): Node.js, Python, Java, Go, Ruby, .NET, PHP, Perl — see also [docs/builder-images.md](docs/builder-images.md).

### Environment Setup

Configure OpenShift cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Verify access:

```bash
oc get projects
```

Copy MCP server definitions from **`rh-developer/.mcp.json`** into your assistant MCP settings. **macOS Podman note:** the **openshift** MCP stanza may use `--userns=keep-id`; Podman on macOS runs in a VM and this can prevent startup. If the server fails to start, remove or adjust the `--userns` arguments in `.mcp.json` per your platform (see upstream README guidance; Linux typically keeps the mapping for `chmod 600` kubeconfigs).
