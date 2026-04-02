### Prerequisites

- Claude Code CLI or IDE extension (or Cursor)
- Red Hat Ansible Automation Platform 2.5+
- AAP API token (Personal Access Token)

### Environment Setup

Configure AAP MCP server and API token:

```bash
export AAP_MCP_SERVER="your-aap-mcp-server.example.com"
export AAP_API_TOKEN="your-personal-access-token"
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-automation
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-automation
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-automation ~/.cursor/plugins/rh-automation
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-automation ~/.cursor/plugins/rh-automation
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-automation ~/.opencode/plugins/rh-automation
```
