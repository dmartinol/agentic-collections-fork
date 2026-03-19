# Red Hat Support Engineer Agentic Collection

Technical support and troubleshooting tools for Red Hat products and platforms.

**Persona**: Development Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-support-engineer collection provides skills for development tasks.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension

### Environment Setup

Environment variables depend on which skills you use. Configure as needed for the Red Hat products and platforms you are troubleshooting.

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-support-engineer
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-support-engineer
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-support-engineer ~/.cursor/plugins/rh-support-engineer
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-support-engineer ~/.cursor/plugins/rh-support-engineer
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-support-engineer ~/.opencode/plugins/rh-support-engineer
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-support-engineer ~/.opencode/plugins/rh-support-engineer
```


## Skills

The pack will provide skills for technical support and troubleshooting (skills in development).






## Sample Workflows


### See collection.yaml

Add workflows in collection.yaml.



## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Main Repository](https://github.com/RHEcosystemAppEng/agentic-collections) - agentic-collections

