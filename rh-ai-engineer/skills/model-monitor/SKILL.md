---
name: model-monitor
description: |
  Configure TrustyAI model monitoring for bias detection and data drift on deployed InferenceServices.

  Use when:
  - "Monitor my model for bias"
  - "Set up drift detection on my inference endpoint"
  - "Configure TrustyAI for my deployed model"
  - "Check if my model has fairness issues"
  - "I need SPD / DIR metrics for my model"

  Handles TrustyAIService deployment, bias metric configuration (SPD, DIR), drift metric configuration (MeanShift, FourierMMD, KS-Test), threshold tuning, and monitoring validation.

  NOT for deploying models (use /model-deploy first).
  NOT for input/output content safety guardrails (use /guardrails-config).
  NOT for infrastructure-level observability (use /ai-observability).
model: inherit
color: blue
---

# /model-monitor Skill

Configure TrustyAI model monitoring for bias detection and data drift on Red Hat OpenShift AI. Deploys TrustyAIService custom resources, configures bias metrics (Statistical Parity Difference, Disparate Impact Ratio) and drift metrics (MeanShift, FourierMMD, KS-Test, Jensen-Shannon) for target InferenceServices, sets alerting thresholds, and validates monitoring is active via Prometheus metrics.

## Prerequisites

**Required MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools** (from openshift):
- `resources_get` (from openshift) - Get TrustyAIService CR status, check CRD availability
- `resources_list` (from openshift) - List TrustyAIService instances, check CRD existence
- `resources_create_or_update` (from openshift) - Create/update TrustyAIService CR, metric configuration ConfigMaps
- `pods_list` (from openshift) - Verify TrustyAI pods are running
- `pods_log` (from openshift) - Retrieve TrustyAI pod logs for troubleshooting
- `events_list` (from openshift) - Check events for TrustyAI deployment issues
- `prometheus_query` (from openshift) - Query TrustyAI metrics (trustyai_spd, trustyai_dir, drift metrics)

**Required MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp))

**Required MCP Tools** (from rhoai):
- `list_inference_services` - List deployed models to identify monitoring targets
- `get_inference_service` - Get InferenceService details (model format, runtime, status)
- `list_data_science_projects` - Validate namespace is an RHOAI Data Science Project

**Optional MCP Server**: `ai-observability` ([AI Observability MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer))

**Optional MCP Tools** (from ai-observability):
- `execute_promql` - Custom PromQL queries for TrustyAI metrics validation

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, KServe, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Additional cluster requirements**:
- TrustyAI operator enabled in the DataScienceCluster CR
- At least one deployed InferenceService to monitor (via `/model-deploy`)
- User Workload Monitoring enabled in OpenShift (for TrustyAI metrics scraping)

## When to Use This Skill

**Use this skill when you need to:**
- Set up bias monitoring (SPD, DIR) for a deployed model
- Configure data drift detection on inference data streams
- Deploy a TrustyAIService instance in a namespace
- Check whether monitoring is active and metrics are flowing
- Tune fairness thresholds or drift sensitivity for an existing monitored model

**Do NOT use this skill when:**
- You need to deploy a model first (use `/model-deploy`)
- You need LLM input/output content safety guardrails (use `/guardrails-config`)
- You want infrastructure-level performance metrics like latency and throughput (use `/ai-observability`)
- You need to troubleshoot a failed model deployment (use `/debug-inference`)

## Workflow

### Step 1: Gather Monitoring Requirements

**Ask the user for:**
- **Target model**: Which InferenceService to monitor (name or "list all")
- **Namespace**: Target namespace
- **Monitoring type**: Bias detection, drift detection, or both
- **For bias monitoring**:
  - Protected attribute (e.g., "gender", "age", "race") -- the feature to check for fairness
  - Favorable outcome -- the model output value considered "positive"
  - Privileged group value -- the value of the protected attribute for the privileged group
  - Unprivileged group value -- the value for the unprivileged group
- **For drift monitoring**:
  - Which drift metrics to enable (MeanShift, FourierMMD, KS-Test, Jensen-Shannon -- default: all)

If user says "list all" or is unsure about target model:

**MCP Tool**: `list_inference_services` (from rhoai)

**Parameters**:
- `namespace`: user-specified namespace - REQUIRED
- `verbosity`: `"standard"` - OPTIONAL

Present InferenceServices:

| Name | Runtime | Ready | URL |
|------|---------|-------|-----|
| [name] | [runtime] | [True/False] | [url] |

**WAIT for user to select which InferenceService to monitor.**

**Present configuration summary:**

| Setting | Value |
|---------|-------|
| Target Model | [isvc-name] |
| Namespace | [namespace] |
| Monitoring Type | [bias / drift / both] |
| Bias: Protected Attribute | [attribute or N/A] |
| Bias: Favorable Outcome | [value or N/A] |
| Drift Metrics | [list or N/A] |

**WAIT for user to confirm or modify these settings.**

### Step 2: Verify TrustyAI Operator Installation

**MCP Tool**: `resources_list` (from openshift)

**Parameters**:
- `apiVersion`: `"apiextensions.k8s.io/v1"` - REQUIRED
- `kind`: `"CustomResourceDefinition"` - REQUIRED

Check for the presence of `trustyaiservices.trustyai.opendatahub.io` CRD.

**Error Handling**:
- If CRD not found: Report "TrustyAI operator is not installed on this cluster. The TrustyAI component must be enabled in the DataScienceCluster CR." Show enablement command: `oc patch datasciencecluster default-dsc --type merge -p '{"spec":{"components":{"trustyai":{"managementState":"Managed"}}}}'`. Offer options: (1) Show enablement instructions, (2) Abort. **WAIT for user decision.**

### Step 3: Check/Create TrustyAIService in Namespace

**Document Consultation** (read before configuring TrustyAI):
1. **Action**: Read [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) using the Read tool to understand CRD spec fields, metric names, and thresholds
2. **Output to user**: "I consulted [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) to understand TrustyAI CRD specifications and metric configuration."

**MCP Tool**: `resources_get` (from openshift)

**Parameters**:
- `apiVersion`: `"trustyai.opendatahub.io/v1alpha1"` - REQUIRED
- `kind`: `"TrustyAIService"` - REQUIRED
- `namespace`: target namespace - REQUIRED
- `name`: `"trustyai-service"` - REQUIRED

**If TrustyAIService exists and is Ready:**
- Report: "TrustyAI service is already deployed and ready in namespace [namespace]."
- Proceed to Step 5.

**If TrustyAIService exists but NOT Ready:**
- Check pod status and events (see Step 4).
- Present diagnostic options. **WAIT for user decision.**

**If TrustyAIService does NOT exist:**
- Inform user: "No TrustyAIService found in namespace [namespace]. I'll create one."

**Prepare TrustyAIService manifest** using the CRD spec from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md):

```yaml
apiVersion: trustyai.opendatahub.io/v1alpha1
kind: TrustyAIService
metadata:
  name: trustyai-service
  namespace: [namespace]
spec:
  storage:
    format: PVC
    folder: /data
    size: 1Gi
  data:
    filename: data.csv
    format: CSV
  metrics:
    schedule: 5s
```

**Display the manifest to the user.** Ask: "Proceed with creating this TrustyAIService? (yes/no/modify)"

**WAIT for explicit confirmation.**

**MCP Tool**: `resources_create_or_update` (from openshift)

**Parameters**:
- `manifest`: the TrustyAIService YAML manifest as JSON string - REQUIRED

**Error Handling**:
- If RBAC error -> Report insufficient permissions, suggest contacting cluster admin
- If quota error -> Report resource quota exceeded

### Step 4: Verify TrustyAI Pods Are Running

**MCP Tool**: `pods_list` (from openshift)

**Parameters**:
- `namespace`: target namespace - REQUIRED
- `labelSelector`: `"app.kubernetes.io/name=trustyai-service"` - REQUIRED

Verify at least one TrustyAI pod is in Running state. Report pod status:

| Pod | Status | Restarts | Age |
|-----|--------|----------|-----|
| [pod-name] | [Running/Pending/Error] | [count] | [age] |

**If pods not ready** (Pending, CrashLoopBackOff, etc.):

**MCP Tool**: `pods_log` (from openshift)
- `namespace`: target namespace, `name`: the TrustyAI pod name

**MCP Tool**: `events_list` (from openshift)
- `namespace`: target namespace

Present findings and options: (1) View full logs, (2) Check events, (3) Delete and recreate TrustyAIService, (4) Abort. **WAIT for user decision. NEVER auto-delete TrustyAIService.**

### Step 5: Configure Bias Metrics

**Condition**: Only when monitoring type includes bias detection.

**Prepare bias metric configuration** using thresholds from [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md).

**MCP Tool**: `resources_create_or_update` (from openshift)

Create a ConfigMap storing the bias metric configuration:

**Parameters**:
- `manifest`: ConfigMap YAML manifest as JSON string - REQUIRED

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: trustyai-bias-config-[isvc-name]
  namespace: [namespace]
  labels:
    app.kubernetes.io/part-of: trustyai
    trustyai.opendatahub.io/target-model: [isvc-name]
data:
  spd-config.json: |
    {
      "modelId": "[isvc-name]",
      "protectedAttribute": "[attribute]",
      "favorableOutcome": [value],
      "outcomeName": "[outcome-field]",
      "privilegedAttribute": [privileged-value],
      "unprivilegedAttribute": [unprivileged-value],
      "metricName": "SPD",
      "thresholdDelta": 0.1
    }
  dir-config.json: |
    {
      "modelId": "[isvc-name]",
      "protectedAttribute": "[attribute]",
      "favorableOutcome": [value],
      "outcomeName": "[outcome-field]",
      "privilegedAttribute": [privileged-value],
      "unprivilegedAttribute": [unprivileged-value],
      "metricName": "DIR",
      "thresholdLower": 0.8,
      "thresholdUpper": 1.2
    }
```

**Display manifest to user.** Explain thresholds:
- **SPD**: Value of 0 = perfect fairness. Threshold delta of 0.1 means alert if |SPD| > 0.1.
- **DIR**: Value of 1.0 = perfect fairness. Alert if DIR < 0.8 or DIR > 1.2.

**Ask**: "Proceed with these bias metric configurations? You can adjust thresholds. (yes/no/modify)"

**WAIT for explicit confirmation.**

### Step 6: Configure Drift Metrics

**Condition**: Only when monitoring type includes drift detection.

**MCP Tool**: `resources_create_or_update` (from openshift)

Create a ConfigMap storing drift metric configuration:

**Parameters**:
- `manifest`: ConfigMap YAML manifest as JSON string - REQUIRED

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: trustyai-drift-config-[isvc-name]
  namespace: [namespace]
  labels:
    app.kubernetes.io/part-of: trustyai
    trustyai.opendatahub.io/target-model: [isvc-name]
data:
  drift-config.json: |
    {
      "modelId": "[isvc-name]",
      "metrics": ["MEANSHIFT", "FOURIERMMD", "KSTEST"],
      "referenceTag": "TRAINING",
      "thresholds": {
        "MEANSHIFT": 0.1,
        "FOURIERMMD": 0.05,
        "KSTEST": 0.05
      }
    }
```

**Display manifest and explain drift metrics:**
- **MeanShift**: Detects shift in mean of feature distributions. Threshold = max allowable mean shift.
- **FourierMMD**: Frequency-domain distribution comparison. Lower threshold = more sensitive.
- **KS-Test**: Kolmogorov-Smirnov test p-value threshold. Below threshold = distribution has drifted.

**Ask**: "Proceed with these drift metric configurations? (yes/no/modify)"

**WAIT for explicit confirmation.**

### Step 7: Validate Monitoring Is Active

Wait 30-60 seconds after configuration, then verify metrics are being produced.

**Option A** (if `openshift` MCP has `prometheus_query`):

**MCP Tool**: `prometheus_query` (from openshift)

**Parameters**:
- `query`: `"trustyai_spd{model=\"[isvc-name]\"}"` - REQUIRED (for bias)

For drift:
- `query`: `"trustyai_meanshift{model=\"[isvc-name]\"}"` - REQUIRED

**Option B** (if `ai-observability` MCP available):

**MCP Tool**: `execute_promql` (from ai-observability)

**Parameters**:
- `query`: `"trustyai_spd{model=\"[isvc-name]\"}"` - REQUIRED
- `time_range`: `"5m"` - OPTIONAL

**If metrics are present**: Report current values and confirm monitoring is active.

**If metrics are NOT present**: This is expected if no inference requests have been made yet. Inform user: "Monitoring is configured but no metric data yet. TrustyAI metrics will appear after the model receives inference requests (~100 requests needed for stable bias metrics). Send test requests to [model-endpoint] to generate initial data."

### Step 8: Summary and Next Steps

Present a monitoring configuration summary:

```
## Model Monitoring Summary: [isvc-name]

| Configuration | Value |
|--------------|-------|
| TrustyAI Service | Running in [namespace] |
| Target Model | [isvc-name] |
| Bias Metrics | SPD (threshold: +/-0.1), DIR (threshold: 0.8-1.2) |
| Drift Metrics | MeanShift, FourierMMD, KS-Test |
| Metric Schedule | Every 5 seconds |
| Status | [Active / Awaiting data] |

### Prometheus Queries for Dashboards

- SPD: `trustyai_spd{model="[isvc-name]"}`
- DIR: `trustyai_dir{model="[isvc-name]"}`
- MeanShift: `trustyai_meanshift{model="[isvc-name]"}`

### Next Steps

- Send inference requests to generate monitoring data
- View metrics in OpenShift AI dashboard or Grafana
- Use `/ai-observability` for infrastructure performance metrics
- Use `/guardrails-config` to add content safety guardrails
```

## Common Issues

For common issues (GPU scheduling, OOMKilled, image pull errors, RBAC), see [common-issues.md](../references/common-issues.md).

### Issue 1: TrustyAI Operator Not Installed

**Error**: `trustyaiservices.trustyai.opendatahub.io` CRD not found

**Cause**: The TrustyAI component is not enabled in the DataScienceCluster CR.

**Solution:**
1. Check DataScienceCluster: `resources_get` for `DataScienceCluster`
2. Enable TrustyAI component: patch the DSC with `spec.components.trustyai.managementState: Managed`
3. Wait for the operator to deploy TrustyAI CRDs
4. Retry the skill

### Issue 2: TrustyAI Pod CrashLoopBackOff

**Error**: TrustyAI pod restarts repeatedly with storage-related errors

**Cause**: PVC for TrustyAI data storage cannot be provisioned, or the storage class is unavailable.

**Solution:**
1. Check PVC status: `resources_list` for PVCs in namespace with TrustyAI labels
2. Verify a default StorageClass exists: `resources_list` for StorageClass
3. If no default StorageClass, specify one in the TrustyAIService CR `spec.storage.storageClass`
4. Check pod logs for specific storage errors

### Issue 3: No Metrics Appearing in Prometheus

**Error**: PromQL queries return empty results even after inference requests

**Cause**: User Workload Monitoring is not enabled, or the TrustyAI ServiceMonitor is missing.

**Solution:**
1. Verify User Workload Monitoring is enabled: check `cluster-monitoring-config` ConfigMap in `openshift-monitoring` namespace for `enableUserWorkload: true`
2. Check that a ServiceMonitor exists for TrustyAI: `resources_list` for ServiceMonitor in the namespace
3. Verify TrustyAI pods expose the `/q/metrics` endpoint
4. Check Prometheus targets for the TrustyAI scrape target

### Issue 4: Bias Metrics Show Insufficient Data

**Error**: SPD/DIR metrics return NaN or insufficient data warnings

**Cause**: Not enough inference requests with the protected attribute have been processed. TrustyAI requires ~100 requests for stable metrics.

**Solution:**
1. Send more inference requests through the model with varied protected attribute values
2. Ensure the inference payload includes the protected attribute field
3. Check TrustyAI logs for data ingestion errors
4. Verify the `protectedAttribute` field name matches the model's input schema exactly

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/model-deploy` - Deploy the InferenceService before configuring monitoring
- `/debug-inference` - Troubleshoot issues found by monitoring alerts
- `/ai-observability` - Infrastructure-level performance metrics (complements TrustyAI fairness metrics)
- `/guardrails-config` - Add content safety guardrails to the monitored model

### Reference Documentation
- [trustyai-metrics-reference.md](references/trustyai-metrics-reference.md) - TrustyAI CRD specs, Prometheus metric names, and threshold guidance

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After gathering requirements (Step 1): confirm monitoring configuration
- Before creating TrustyAIService (Step 3): display manifest, confirm creation
- Before configuring bias metrics (Step 5): confirm metric parameters and thresholds
- Before configuring drift metrics (Step 6): confirm metric parameters and thresholds
- On TrustyAI pod failure (Step 4): present diagnostic options, wait for user decision
- **NEVER** auto-delete TrustyAIService or metric configurations
- **NEVER** modify fairness thresholds without explicit user confirmation
