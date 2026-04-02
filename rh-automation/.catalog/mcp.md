Six HTTP MCP servers (see **`rh-automation/.mcp.json`** and [AAP MCP Server](https://github.com/ansible/aap-mcp-server)):

| Server | Purpose |
|--------|---------|
| **aap-mcp-job-management** | Job templates, launches, events, workflows |
| **aap-mcp-inventory-management** | Inventories, hosts, groups, facts |
| **aap-mcp-configuration** | Notifications, execution environments, platform settings |
| **aap-mcp-security-compliance** | Credentials, credential types, testing |
| **aap-mcp-system-monitoring** | Instance groups, activity stream, mesh, status |
| **aap-mcp-user-management** | Users, teams, organizations, RBAC |

Full governance audits require reachability across **all six**; execution paths may use a subset. Set **`AAP_MCP_SERVER`** and **`AAP_API_TOKEN`** as documented under Quick Start.
