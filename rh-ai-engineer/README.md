# Red Hat AI Engineer Agentic Collection

Automation tools for AI/ML engineers working with Red Hat OpenShift AI (RHOAI). Deploy and manage models, pipelines, registries, workbenches, and serving runtimes on OpenShift AI.

**Persona**: AI/ML Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

The rh-ai-engineer collection provides skills for deploying and managing AI/ML models,
pipelines, workbenches, and serving runtimes on Red Hat OpenShift AI.


## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- Red Hat OpenShift AI (RHOAI) cluster with model serving capabilities
- `oc` CLI and `KUBECONFIG` configured for cluster access

### Environment Setup

Configure OpenShift AI cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Verify access to OpenShift AI:

```bash
oc get datascienceprojects -A
```

### Installation (Claude Code)

Install the collection as a Claude Code plugin:

```bash
claude plugin marketplace add https://github.com/RHEcosystemAppEng/agentic-collections
claude plugin install rh-ai-engineer
```

Or for local development:

```bash
claude plugin marketplace add /path/to/agentic-collections
claude plugin install rh-ai-engineer
```

### Installation (Cursor)

Cursor does not support direct marketplace install via CLI. Clone the repository and copy the collection:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-ai-engineer ~/.cursor/plugins/rh-ai-engineer
```

Or download and extract:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-ai-engineer ~/.cursor/plugins/rh-ai-engineer
```

### Installation (Open Code)

Open Code does not support direct marketplace install via CLI. Clone or download the repository:

```bash
git clone https://github.com/RHEcosystemAppEng/agentic-collections.git
cp -r agentic-collections/rh-ai-engineer ~/.opencode/plugins/rh-ai-engineer
```

Or with wget:

```bash
wget -qO- https://github.com/RHEcosystemAppEng/agentic-collections/archive/refs/heads/main.tar.gz | tar xz
cp -r agentic-collections-main/rh-ai-engineer ~/.opencode/plugins/rh-ai-engineer
```


## Skills

The pack provides 11 skills for deploying and managing AI/ML models on Red Hat OpenShift AI.



### ds-project-setup - Data Science Project Setup

Set up data science projects on OpenShift AI with namespace setup, S3 data connections, pipeline server, and model serving enablement.

**Use when:**
- "Create a new data science project"
- "Set up project for model development"
- "Configure OpenShift AI project"
- "Add an S3 data connection to my project"
- "Configure the pipeline server"

**What it does:**
- Creates and configures DS projects with RHOAI labels
- Sets up S3-compatible data connections
- Configures pipeline server and model serving
- Sets up resource quotas and access permissions



### workbench-manage - Workbench Management

Manage OpenShift AI workbenches for interactive development and experimentation.

**Use when:**
- "Create a workbench"
- "Manage my Jupyter workbench"
- "Configure development environment"

**What it does:**
- Creates and manages workbenches
- Configures notebook environments
- Handles resource allocation



### model-deploy - Model Deployment

Deploy AI/ML models to OpenShift AI serving runtimes.

**Use when:**
- "Deploy this model"
- "Serve the trained model"
- "Create inference endpoint"

**What it does:**
- Deploys models to serving runtimes
- Configures inference endpoints
- Manages model versions



### model-registry - Model Registry

Register, version, and promote ML models in the Model Registry across environments.

**Use when:**
- "Register a new model in the registry"
- "List registered models"
- "What versions exist for my model?"
- "Promote a model from dev to production"

**What it does:**
- Handles model registration and versioning
- Manages metadata and artifact tracking
- Supports cross-environment promotion



### pipeline-manage - Pipeline Management

Create, run, schedule, and monitor Data Science Pipelines (Kubeflow Pipelines 2.0).

**Use when:**
- "Run a pipeline in my project"
- "Schedule a recurring pipeline"
- "Check my pipeline run status"
- "List pipeline runs and their logs"

**What it does:**
- Submits pipeline runs from YAML
- Schedules recurring runs with cron
- Monitors execution and step logs



### nim-setup - NIM (NVIDIA Inference Microservices) Setup

Set up NVIDIA Inference Microservices for GPU-accelerated model serving.

**Use when:**
- "Configure NIM for model serving"
- "Set up GPU inference"
- "Deploy with NVIDIA NIM"

**What it does:**
- Configures NIM integration
- Sets up GPU resources
- Manages inference microservices



### serving-runtime-config - Serving Runtime Configuration

Configure serving runtimes for model inference on OpenShift AI.

**Use when:**
- "Configure serving runtime"
- "Set up inference configuration"
- "Adjust model serving parameters"

**What it does:**
- Configures runtime parameters
- Manages resource allocation
- Sets up scaling and replicas



### debug-inference - Inference Debugging

Diagnose and troubleshoot model inference issues on OpenShift AI.

**Use when:**
- "Why is inference failing?"
- "Debug model serving"
- "Inference errors"

**What it does:**
- Analyzes inference logs
- Checks endpoint health
- Identifies configuration issues



### ai-observability - AI Observability

Monitor and observe AI/ML workloads, model performance, and inference metrics.

**Use when:**
- "Show model performance metrics"
- "Monitor inference latency"
- "AI workload observability"

**What it does:**
- Collects and displays metrics
- Monitors inference performance
- Tracks model usage and latency



### model-monitor - TrustyAI Model Monitoring

Configure TrustyAI bias detection (SPD, DIR) and data drift monitoring on deployed InferenceServices.

**Use when:**
- "Monitor my model for bias"
- "Set up drift detection on my inference endpoint"
- "Configure TrustyAI for my deployed model"
- "Check if my model has fairness issues"

**What it does:**
- Deploys TrustyAIService CR
- Configures bias metrics (SPD, DIR) and drift metrics
- Validates monitoring and threshold tuning



### guardrails-config - TrustyAI Guardrails Orchestrator

Deploy TrustyAI Guardrails Orchestrator with input/output content safety detectors for LLM endpoints.

**Use when:**
- "Add guardrails to my LLM endpoint"
- "Set up content safety for my model"
- "Configure PII detection on my inference endpoint"
- "Block prompt injection attacks"

**What it does:**
- Deploys GuardrailsOrchestrator CR
- Configures detectors (content safety, PII, prompt injection, toxicity)
- Manages orchestration policies and guarded endpoint validation




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| "Deploy Llama 3 on my cluster" or "Create inference endpoint" | model-deploy | Deploys AI/ML models to OpenShift AI serving runtimes (vLLM, NIM, Caikit+TGIS). |
| "Set up NIM on my cluster" or "Configure NGC credentials for NIM" | nim-setup | Configures NVIDIA NIM platform on OpenShift AI for GPU-accelerated inference. |
| "Why is inference failing?" or "Debug model serving" | debug-inference | Troubleshoots failed or slow InferenceService deployments. |
| "Show model performance metrics" or "Monitor inference latency" | ai-observability | Analyzes model performance, GPU utilization, and cluster health. |
| "Create a new data science project" or "Set up project for model development" | ds-project-setup | Creates and configures Data Science Projects on OpenShift AI. |
| "Monitor my model for bias" or "Set up drift detection" | model-monitor | Configures TrustyAI bias (SPD, DIR) and drift monitoring on deployed InferenceServices. |
| "Add guardrails to my LLM" or "Set up content safety" | guardrails-config | Deploys TrustyAI Guardrails Orchestrator with input/output content safety detectors. |




## Sample Workflows


### Deploy a model from registry

1. Use `/model-registry` to list and select a model version
2. Use `/model-deploy` to deploy the selected model to a serving runtime
3. Use `/ai-observability` to monitor inference performance



### Set up new data science project

1. Use `/ds-project-setup` to create project with data connections and pipeline server
2. Use `/workbench-manage` to create a Jupyter workbench for development
3. Use `/pipeline-manage` to run and monitor pipelines




## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Main Repository](https://github.com/RHEcosystemAppEng/agentic-collections) - agentic-collections

