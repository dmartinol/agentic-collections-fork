### Prerequisites

- Claude Code CLI or IDE extension
- Podman or Docker installed
- Red Hat Lightspeed service account ([setup guide](https://console.redhat.com/))

### Environment Setup

Configure Red Hat Lightspeed credentials:

```bash
export LIGHTSPEED_CLIENT_ID="your-service-account-client-id"
export LIGHTSPEED_CLIENT_SECRET="your-service-account-client-secret"
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-sre
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-sre
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-sre ~/.cursor/plugins/rh-sre
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-sre ~/.cursor/plugins/rh-sre
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-sre ~/.opencode/plugins/rh-sre
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-sre ~/.opencode/plugins/rh-sre
```
