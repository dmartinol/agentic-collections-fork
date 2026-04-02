<!--
  GENERATED FILE — do not edit manually.
  Source of truth: rh-ai-engineer/collection.yaml
  Regenerate with: make generate-catalog
-->

# Red Hat AI Engineer Agentic Collection

Automation tools for AI/ML engineers working with Red Hat OpenShift AI (RHOAI). Deploy and manage models, pipelines, registries, workbenches, and serving runtimes on OpenShift AI.

**Persona**: AI/ML Engineer
**Marketplaces**: Claude Code, Cursor

## Overview

Deploy and operate models on OpenShift AI with skills for **data science projects**, **workbenches**,
**model serving** (KServe / vLLM / NIM), **registries**, **pipelines**, **custom runtimes**,
**debugging**, **observability**, **TrustyAI monitoring**, and **guardrails**.


## Quick Start

### Prerequisites

- Claude Code CLI or IDE extension
- **`podman`** (or Docker) for containerized MCP servers where configured in `.mcp.json`
- **`oc`** CLI and **`KUBECONFIG`** for cluster access
- OpenShift cluster with **Red Hat OpenShift AI** operator installed and **KServe** model serving available
- **GPU nodes** for GPU-accelerated inference (see [known-model-profiles.md](docs/references/known-model-profiles.md) for sizing hints)

**For NVIDIA NIM deployments:** NVIDIA GPU Operator, Node Feature Discovery (NFD), and an **NGC API key** (see **`/nim-setup`** and [NIM on OpenShift AI](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed)).

### Environment Setup

Configure OpenShift AI cluster access:

```bash
export KUBECONFIG="/path/to/your/kubeconfig"
```

Optional observability MCP URL (when using the remote summarizer pattern):

```bash
export AI_OBSERVABILITY_MCP_URL="https://your-observability-mcp.example"
```

Verify access to OpenShift AI:

```bash
oc get datascienceprojects -A
```

MCP definitions live in **`rh-ai-engineer/.mcp.json`** — copy entries into Claude Code `/mcp` or settings; use **`${...}`** placeholders only for secrets.

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

The pack provides 11 skills for OpenShift AI workflows from project bootstrap through guarded inference.



### ds-project-setup - Data Science Project Setup

Create and configure Data Science Projects with namespaces, S3 data connections, pipeline server prep, and model serving enablement.

**Use when:** "Create a data science project", "Add S3 data connection", "Enable model serving on my project".

**What it does:** Applies RHOAI labels, wiring for pipelines and serving; does not deploy models or workbenches.



### workbench-manage - Workbench Management

Create and manage Jupyter workbenches—images, resources, PVCs, start/stop, and safe deletion.

**Use when:** "Create a notebook workbench", "Start my Jupyter server", "List notebook images".

**What it does:** Drives Notebook CR lifecycle while separating concerns from `/model-deploy`.



### model-deploy - Model Deployment and Serving

Deploy models with KServe using vLLM, NVIDIA NIM, or Caikit+TGIS; validates GPUs and monitors rollouts.

**Use when:** "Deploy Llama on OpenShift AI", "Create an InferenceService", "Serve with vLLM".

**What it does:** Selects runtimes, builds CRs, and monitors readiness; run `/nim-setup` first for NIM-only platforms.



### model-registry - Model Registry Operations

Register, version, catalog, and promote models across environments.

**Use when:** "Register this model", "Promote version to prod", "Show model artifacts".

**What it does:** Integrates with OpenShift AI Model Registry APIs and catalog views.



### pipeline-manage - Data Science Pipelines

Run, schedule, and monitor Kubeflow Pipelines 2.0 workloads on OpenShift AI.

**Use when:** "Run my pipeline YAML", "Schedule a nightly training pipeline", "Why did this PipelineRun fail?".

**What it does:** Manages DSPA prerequisites, submissions, cron schedules, and logs.



### nim-setup - NVIDIA NIM Platform Setup

Configure NGC credentials and NIM Account CRs so NIM-based InferenceServices can run.

**Use when:** "Set up NIM", "Configure NVIDIA NIM before deploying models".

**What it does:** One-time platform prerequisites prior to `/model-deploy` with NIM.



### serving-runtime-config - Custom Serving Runtimes

List, create, or customize `ServingRuntime` CRs for frameworks beyond stock templates.

**Use when:** "Create a custom runtime", "Need ONNX or Triton runtime", "Tune vLLM runtime parameters".

**What it does:** Validates compatibility and applies runtime manifests before serving models.



### debug-inference - Inference Troubleshooting

Diagnose stuck or unhealthy InferenceServices using conditions, events, logs, and GPU checks.

**Use when:** "InferenceService not ready", "Model endpoint errors", "GPU not scheduling".

**What it does:** Structured triage with optional observability correlations.



### ai-observability - AI Observability

Query vLLM metrics, GPU utilization, cluster health, and distributed traces.

**Use when:** "How is my model performing?", "Show GPU usage", "Trace a slow request".

**What it does:** Read-only routing to observability backends (optional MCP).



### model-monitor - TrustyAI Model Monitoring

Configure bias and drift monitoring (SPD, DIR, drift detectors) for deployed models.

**Use when:** "Enable TrustyAI monitoring", "Detect drift on my endpoint", "SPD/DIR metrics".

**What it does:** Deploys TrustyAIService configs after `/model-deploy` completes.



### guardrails-config - TrustyAI Guardrails

Deploy guardrails orchestrators with PII, toxicity, and prompt-injection detectors.

**Use when:** "Add guardrails to my LLM", "Need a secured inference route".

**What it does:** Creates GuardrailsOrchestrator policies atop existing InferenceServices.




## Skills Decision Guide

| User request | Skill to use | Reason |
|--------------|--------------|--------|
| New data science project, data connection, pipeline server, enable model serving | ds-project-setup | Bootstraps namespaces, storage, DSPA prerequisites, and serving configuration. |
| Jupyter workbench, notebook images, start or stop a workbench | workbench-manage | Manages Notebook CR lifecycle separate from model deployment. |
| Deploy a model, InferenceService, vLLM, KServe, NIM runtime | model-deploy | Creates and rolls out InferenceService resources with runtime selection. |
| Model registry, catalog, versions, promote a model | model-registry | Registers artifacts and versions for governance and promotion flows. |
| Kubeflow pipeline, PipelineRun, schedule or troubleshoot DSP pipelines | pipeline-manage | Submits runs, schedules jobs, and surfaces pipeline logs. |
| First-time NIM platform, NGC credentials, NIM Account CR | nim-setup | One-time prerequisite before `/model-deploy` with NVIDIA NIM. |
| Custom ServingRuntime, runtime templates, specialized frameworks | serving-runtime-config | Creates or customizes ServingRuntime CRs before deployment. |
| InferenceService stuck, failing rollout, inference errors, GPU scheduling | debug-inference | Progressive diagnosis of deployments, events, and pods. |
| Model latency, GPU metrics, cluster health, tracing | ai-observability | Read-only observability across metrics and traces. |
| TrustyAI bias, drift, SPD, DIR on an InferenceService | model-monitor | Configures TrustyAI monitoring after a model is deployed. |
| Content safety, PII, guardrails, protected inference endpoint | guardrails-config | Deploys GuardrailsOrchestrator and detectors on top of a served model. |



## Documentation

### Supported runtimes

| Runtime | Typical use | Setup |
|---------|------------|--------|
| **vLLM** | Open-source LLMs (Llama, Granite, Mixtral, Mistral) | None beyond cluster/serving |
| **NVIDIA NIM** | TensorRT-LLM on NVIDIA GPUs | Run **`/nim-setup`** first |
| **Caikit+TGIS** | Caikit-format models, gRPC | Model conversion as required |

Full comparison: **[supported-runtimes.md](docs/references/supported-runtimes.md)**.

### Example model / GPU profiles

| Model | Params | Min GPUs (typical) | Default runtime |
|-------|--------|--------------------|-----------------|
| Llama 3.1 8B | 8B | 1× (16GB VRAM) | vLLM |
| Llama 3.1 70B | 70B | 4× A100 80GB | vLLM / NIM |
| Granite 3.1 8B | 8B | 1× (16GB VRAM) | vLLM |
| Mixtral 8x7B | 46.7B MoE | 2× A100 80GB | vLLM |
| Mistral 7B | 7B | 1× (16GB VRAM) | vLLM |

Extended tables and guidance: **[known-model-profiles.md](docs/references/known-model-profiles.md)**. Models not listed are still supported via product docs and live cluster checks.

### In-repo examples

- NIM walkthrough: [nim-setup.md](docs/examples/nim-setup.md) (also linked from **References** below).


## MCP Server Integrations

| Server | Type | Requirement | Role |
|--------|------|-------------|------|
| **`openshift`** | Container (e.g. podman) | **Required** | Kubernetes CRUD, pods, logs, events — foundation for all skills. |
| **`rhoai`** | Local process (e.g. `uvx`) | **Preferred** | RHOAI-focused helpers (deployments, runtimes, projects); skills **fall back to openshift** on auth/API errors. See [opendatahub-io/rhoai-mcp](https://github.com/opendatahub-io/rhoai-mcp). |
| **`ai-observability`** | Remote HTTP | **Optional** | Metrics, GPU checks, tracing; skipped if unset. See [ai-observability-summarizer MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer/tree/main/src/mcp_server). |

The **`openshift`** server is the reliable baseline. **`rhoai`** speeds YAML-light flows; when it fails, skills transparently use equivalent OpenShift operations (refresh `oc login` if tokens expire).

## Sample Workflows


### Bootstrap then deploy a model

User: "I need a new OpenShift AI project and a deployed model"
- **ds-project-setup** creates the project, connections, and serving prerequisites
- **workbench-manage** (optional) attaches a notebook for experimentation
- **model-deploy** rolls out the InferenceService; use **nim-setup** first if using NVIDIA NIM



### Harden and monitor production inference

User: "Harden monitoring and guardrails on my production model"
- **model-deploy** ensures the model is ready
- **ai-observability** validates latency, GPU, and trace signals
- **model-monitor** or **guardrails-config** layers TrustyAI monitoring or guardrails as required



### Debug a failed rollout

User: "My InferenceService rollout failed—help me debug"
- **debug-inference** isolates failing pods, events, or resources
- Re-run **model-deploy** or adjust **serving-runtime-config** based on findings



### Deploy a model from registry

User: "Deploy model v1.2 from the registry to production"
- **model-registry** lists and selects a model version
- **model-deploy** deploys the selected model to a serving runtime
- **ai-observability** monitors inference performance



### Set up a new data science project

User: "Create a new data science project with a Jupyter workbench"
- **ds-project-setup** creates the project with data connections and pipeline server
- **workbench-manage** creates a Jupyter workbench for development
- **pipeline-manage** runs and monitors pipelines




## Security Model

- Never print NGC keys, kubeconfig, or pull secrets — only confirm that required env vars exist.
- Follow each skill's confirmation gates before creating or deleting DataScienceProject, InferenceService, or storage resources.
- Optional **`ai-observability`** must not receive production secrets in URLs; use network policies and TLS as appropriate.

## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Red Hat OpenShift AI Documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed) - RHOAI product documentation for model serving, pipelines, and workbenches.


- [Known model hardware profiles (in-repo)](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed/latest/html-single/red_hat_openshift_ai_self_managed) - Parameter counts, GPU sizing, and runtime notes collated for common models.


- [OpenShift AI Model Serving](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed/latest/html-single/red_hat_openshift_ai_self_managed) - InferenceService, runtimes, and model deployment.


- [NVIDIA NIM on OpenShift AI](https://docs.nvidia.com/nim/) - NVIDIA Inference Microservices for GPU-accelerated serving.

