# Red Hat Developer Agentic Pack

A Claude Code plugin for building and deploying applications on Red Hat platforms.

## Skills

| Command                  | Description                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| `/detect-project`      | Analyze project to detect language, framework, and version                                 |
| `/recommend-image`     | Recommend optimal S2I builder or base image                                                |
| `/s2i-build`           | Build container images using Source-to-Image on OpenShift                                  |
| `/deploy`              | Deploy container images to OpenShift with Service and Route                                |
| `/helm-deploy`         | Deploy applications using Helm charts                                                      |
| `/rhel-deploy`         | Deploy to standalone RHEL/Fedora systems via SSH                                           |
| `/containerize-deploy` | End-to-end workflow from source to running app (use if not sure which strategy to choose)) |

## Prerequisites

- OpenShift cluster access (for S2I and OpenShift deployments)
- Podman installed locally
- GitHub personal access token (for GitHub integration)

## MCP Servers

- **openshift** - OpenShift cluster management and Helm deployments
- **podman** - Container image management and local builds
- **github** - Repository browsing and code analysis

### Building the OpenShift MCP Server Image

The OpenShift MCP server is not yet published to public registries, so you need to build it locally before using this plugin.

```bash
# Clone the repository
git clone https://github.com/openshift/openshift-mcp-server.git
cd openshift-mcp-server

# Build the container image
podman build -t localhost/openshift-mcp-server:latest -f Dockerfile .

# Verify the image
podman images localhost/openshift-mcp-server:latest
```

Once built, the OpenShift MCP tools will be available when you restart the coding agent.

## Supported Languages

Node.js, Python, Java, Go, Ruby, .NET, PHP, Perl

## Installation

Add this plugin to your Claude Code configuration.
