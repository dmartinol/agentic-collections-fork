- Never print kubeconfig, GitHub tokens, or Lightspeed client secrets.
- **openshift** MCP user-namespace mapping can affect kubeconfig readability on some hosts; fix MCP config rather than loosening secret file permissions.
- Destructive changes require explicit user approval per skill workflows.

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-developer
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-developer
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-developer ~/.cursor/plugins/rh-developer
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-developer ~/.cursor/plugins/rh-developer
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-developer ~/.opencode/plugins/rh-developer
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-developer ~/.opencode/plugins/rh-developer
```
