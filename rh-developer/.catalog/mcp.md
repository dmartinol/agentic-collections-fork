| Server | Role |
|--------|------|
| **openshift** | Cluster CRUD, builds, deployments, Helm on OpenShift. |
| **podman** | Local images and container tooling. |
| **github** | Repository browse/analysis (e.g. **`/detect-project`** from GitHub URLs). |
| **lightspeed-mcp** | Optional Insights vulnerability/advisor context for RHEL paths. |

Configure all via **`rh-developer/.mcp.json`**; skills must not call MCP tools directly.
