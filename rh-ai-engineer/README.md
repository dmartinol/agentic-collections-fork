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

Skills rely on **`openshift`** (required), **`rhoai`** (preferred), and optional **`ai-observability`** MCP servers defined in `rh-ai-engineer/.mcp.json`. Copy entries into your Claude Code MCP settings; use `${...}` env placeholders only.

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




## Sample Workflows


### Bootstrap then deploy a model

1. **ds-project-setup** — create the project, connections, and serving prerequisites.
2. **workbench-manage** (optional) — attach a notebook for experimentation.
3. **model-deploy** — roll out the InferenceService; use **nim-setup** first if using NVIDIA NIM.



### Harden and monitor production inference

1. **model-deploy** — ensure the model is ready.
2. **ai-observability** — validate latency, GPU, and trace signals.
3. **model-monitor** or **guardrails-config** — layer TrustyAI monitoring or guardrails as required.



### Debug a failed rollout

1. **debug-inference** — isolate failing pods, events, or resources.
2. Re-run **model-deploy** or adjust **serving-runtime-config** based on findings.



### Deploy a model from registry

1. Use **model-registry** to list and select a model version.
2. Use **model-deploy** to deploy the selected model to a serving runtime.
3. Use **ai-observability** to monitor inference performance.



### Set up a new data science project

1. Use **ds-project-setup** to create the project with data connections and pipeline server.
2. Use **workbench-manage** to create a Jupyter workbench for development.
3. Use **pipeline-manage** to run and monitor pipelines.




## License


[Apache-2.0](https://www.redhat.com/en/about/agreements)


## References


- [Red Hat OpenShift AI Documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed) - RHOAI product documentation for model serving, pipelines, and workbenches.


- [OpenShift AI Model Serving](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self_managed/latest/html-single/red_hat_openshift_ai_self_managed) - InferenceService, runtimes, and model deployment.


- [NVIDIA NIM on OpenShift AI](https://docs.nvidia.com/nim/) - NVIDIA Inference Microservices for GPU-accelerated serving.

