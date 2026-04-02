The pack uses **openshift-virtualization** (OpenShift MCP server) as defined in **`.mcp.json`**. The server talks to the cluster Kubernetes API using your kubeconfig.

- Requires OpenShift **4.19+** with OpenShift Virtualization installed.
- Build the MCP image from [openshift/openshift-mcp-server](https://github.com/openshift/openshift-mcp-server) if you do not use a pre-built image (see Quick Start).
