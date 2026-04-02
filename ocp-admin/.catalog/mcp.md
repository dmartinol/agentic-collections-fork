Skills wrap MCP servers defined in **`.mcp.json`** (copy entries into Claude Code `/mcp` or your settings file). Typical layout:

- **openshift-self-managed** — Assisted Installer API for **cluster-creator** / parts of **cluster-inventory** (self-managed OCP, SNO). Requires `OFFLINE_TOKEN`.
- **openshift-ocm-managed** — OpenShift Cluster Manager API for ROSA, ARO, OSD in **cluster-inventory**. Requires `OFFLINE_TOKEN`.
- **openshift-administration** — Kubernetes/OpenShift access for **cluster-report** (node and workload metrics). Requires `KUBECONFIG`.

Images and commands reference `ocp-admin/.mcp.json`; use Podman or Docker as documented there.
