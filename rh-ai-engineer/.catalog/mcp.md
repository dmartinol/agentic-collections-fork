| Server | Type | Requirement | Role |
|--------|------|-------------|------|
| **`openshift`** | Container (e.g. podman) | **Required** | Kubernetes CRUD, pods, logs, events — foundation for all skills. |
| **`rhoai`** | Local process (e.g. `uvx`) | **Preferred** | RHOAI-focused helpers (deployments, runtimes, projects); skills **fall back to openshift** on auth/API errors. See [opendatahub-io/rhoai-mcp](https://github.com/opendatahub-io/rhoai-mcp). |
| **`ai-observability`** | Remote HTTP | **Optional** | Metrics, GPU checks, tracing; skipped if unset. See [ai-observability-summarizer MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer/tree/main/src/mcp_server). |

The **`openshift`** server is the reliable baseline. **`rhoai`** speeds YAML-light flows; when it fails, skills transparently use equivalent OpenShift operations (refresh `oc login` if tokens expire).
