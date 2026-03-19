# Red Hat Developer Agentic Collection

Plugins for building and deploying applications on Red Hat platforms.

**Persona**: Development Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-developer collection provides skills for development tasks.

## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- OpenShift cluster with build and deployment capabilities
- `oc` CLI and `KUBECONFIG` configured for cluster access

### Environment Setup

Configure OpenShift cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Verify access:

```bash
oc get projects
```

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


## Skills

The pack provides 14 skills for building and deploying applications on Red Hat platforms, including one orchestration skill for end-to-end containerization.


## Orchestration Skill


### containerize-deploy - End-to-End Containerization and Deployment

Complete workflow for containerizing and deploying applications to OpenShift or standalone RHEL systems.

**Use when:**
- Containerize and deploy this app
- Build and deploy to OpenShift
- Full deployment from source

**Workflow:**
1. Detect project (detect-project skill)
2. Build image (s2i-build skill)
3. Deploy (deploy, helm-deploy, or rhel-deploy skill based on target)

**Capabilities:**
- Automatic project detection
- S2I or custom build
- OpenShift or RHEL deployment targets





### detect-project - Project Analysis

Analyze a project folder or GitHub repository to detect programming language, framework, and version requirements.

**Use when:**
- What language is this project?
- Detect the framework for this app
- Analyze project for containerization

**What it does:**
- Detects language and framework
- Identifies build requirements
- Recommends S2I builder images



### recommend-image - Builder Image Recommendation

Recommend the optimal S2I builder image or container base image for a project.

**Use when:**
- What S2I image should I use?
- Recommend a builder for this Node.js app
- Best base image for Python project

**What it does:**
- Analyzes project requirements
- Recommends images based on language, security, target
- Supports OpenShift and standalone deployments



### s2i-build - Source-to-Image Build

Create BuildConfig and ImageStream resources and trigger S2I builds on OpenShift.

**Use when:**
- Build this app with S2I
- Create a container image from source
- Build the project on the cluster

**What it does:**
- Creates BuildConfig and ImageStream
- Triggers S2I build
- Handles build logs and status



### deploy - OpenShift Deployment

Create Kubernetes Deployment, Service, and Route resources to deploy and expose an application.

**Use when:**
- Deploy this image to OpenShift
- Expose the app with a route
- Create deployment for the built image

**What it does:**
- Creates Deployment, Service, Route
- Handles port detection
- Exposes application externally



### helm-deploy - Helm Chart Deployment

Deploy applications to OpenShift using Helm charts.

**Use when:**
- Deploy with Helm
- Install this Helm chart
- Deploy using the chart in the project

**What it does:**
- Installs Helm charts
- Supports custom values
- Manages chart upgrades



### rhel-deploy - RHEL Standalone Deployment

Deploy applications to standalone RHEL/Fedora/CentOS systems using Podman or native packages.

**Use when:**
- Deploy to RHEL server
- Run this on a bare metal system
- Install on Fedora

**What it does:**
- Uses Podman with systemd or native packages
- Configures for standalone systems
- Handles non-OpenShift targets



### validate-environment - Environment Validation

Check and report the status of required tools and environment for rh-developer skills.

**Use when:**
- Validate my environment
- Check if oc and helm are installed
- Verify cluster connectivity

**What it does:**
- Validates tool installation (oc, helm, podman, git, skopeo)
- Checks cluster connectivity
- Reports permissions and configuration



### debug-pod - Pod Failure Diagnosis

Diagnose pod failures on OpenShift including CrashLoopBackOff, ImagePullBackOff, OOMKilled, and pending pods.

**Use when:**
- Why is this pod failing?
- Debug CrashLoopBackOff
- Pod won't start

**What it does:**
- Analyzes pod status and events
- Retrieves current and previous logs
- Checks resource limits and image pull



### debug-build - Build Failure Diagnosis

Diagnose OpenShift build failures including S2I builds, Docker/Podman builds, and BuildConfig issues.

**Use when:**
- Why did the build fail?
- Debug S2I build
- BuildConfig not working

**What it does:**
- Validates BuildConfig
- Analyzes build pod logs
- Checks registry authentication



### debug-container - Container Diagnosis

Diagnose local container issues with Podman/Docker including image pull errors, container startup failures, and OOM kills.

**Use when:**
- Container won't start
- Image pull failed
- Debug Podman container

**What it does:**
- Inspects container configuration
- Analyzes logs and events
- Identifies startup and resource issues



### debug-network - Network Connectivity Diagnosis

Diagnose OpenShift service connectivity issues including DNS, service endpoints, routes, and network policies.

**Use when:**
- Service not reachable
- DNS resolution failing
- Debug connectivity between pods

**What it does:**
- Verifies service endpoints
- Checks route and ingress
- Analyzes network policies



### debug-pipeline - Pipeline Failure Diagnosis

Diagnose OpenShift Pipelines (Tekton) CI/CD failures including PipelineRun and TaskRun errors.

**Use when:**
- Pipeline failed
- Debug Tekton PipelineRun
- TaskRun step error

**What it does:**
- Analyzes PipelineRun and TaskRun
- Checks workspace and PVC binding
- Identifies authentication issues



### debug-rhel - RHEL System Diagnosis

Diagnose RHEL system issues including systemd failures, SELinux denials, firewall blocking, and resource problems.

**Use when:**
- Service won't start on RHEL
- SELinux blocking
- Debug systemd unit

**What it does:**
- Analyzes journalctl logs
- Checks SELinux denials
- Verifies firewall and resources




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "Containerize and deploy this app" or "Build and deploy to OpenShift" | containerize-deploy | End-to-end workflow from source to running app; orchestrates detect-project, s2i-build, deploy. |
| "What language is this project?" or "Detect framework for this app" | detect-project | Analyzes project to detect language, framework, and version requirements. |
| "Why is this pod failing?" or "Debug CrashLoopBackOff" | debug-pod | Diagnoses pod failures on OpenShift (CrashLoopBackOff, ImagePullBackOff, OOMKilled). |
| "Why did the build fail?" or "Debug S2I build" | debug-build | Diagnoses OpenShift build failures including S2I builds and BuildConfig issues. |
| "What S2I image should I use?" or "Recommend builder for Node.js" | recommend-image | Recommends optimal S2I builder or base image based on project requirements. |




## Sample Workflows


### Source-to-Image Build and Deploy

User: "Containerize this app and deploy it to OpenShift"
- containerize-deploy skill:
  1. Detects project (detect-project)
  2. Selects deployment target (OpenShift or RHEL)
  3. Builds image (s2i-build or Podman)
  4. Deploys to cluster (deploy)
  5. User confirmation at each phase



### Source-to-Image Build

User: "Build a container from this source code"
- detect-project skill identifies language and framework
- s2i-build skill builds container image
- deploy skill deploys to OpenShift



### Helm Chart Deployment

User: "Deploy this Helm chart to OpenShift"
- detect-project skill (if Helm chart detected) or provide chart path
- helm-deploy skill deploys with release name and namespace




## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [OpenShift Source-to-Image (S2I)](https://docs.openshift.com/container-platform/latest/openshift_images/using_images/using-s21-images.html) - S2I builder images and language detection.


- [Red Hat Container Catalog](https://catalog.redhat.com/software/containers/search) - UBI images and S2I builders.


- [Red Hat Universal Base Images](https://developers.redhat.com/products/rhel/ubi) - UBI9 images and language runtimes.


- [OpenShift Deployments](https://docs.openshift.com/container-platform/latest/applications/deployments/deployment-strategies.html) - Deployment strategies and application lifecycle.

