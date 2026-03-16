---
title: TrustyAI Metrics Reference
category: references
tags: [trustyai, bias, drift, monitoring, metrics, prometheus]
semantic_keywords: [TrustyAI CRD, bias metric names, drift metric names, prometheus queries, SPD threshold, DIR threshold]
use_cases: [model-monitor]
last_updated: 2026-03-16
---

# TrustyAI Metrics Reference

Non-inferable specifications for TrustyAI monitoring on OpenShift AI. The agent should use this as the authoritative source for CRD fields, Prometheus metric names, and domain-specific thresholds.

## TrustyAIService CRD

```yaml
apiVersion: trustyai.opendatahub.io/v1alpha1
kind: TrustyAIService
metadata:
  name: trustyai-service
  namespace: <namespace>
spec:
  storage:
    format: PVC          # PVC or DATABASE
    folder: /data
    size: 1Gi
  data:
    filename: data.csv
    format: CSV
  metrics:
    schedule: 5s         # metric computation interval
  replicas: 1
```

## Cluster Enablement

- **DSC path**: `spec.components.trustyai.managementState: Managed` on the `DataScienceCluster` CR
- **CRD name**: `trustyaiservices.trustyai.opendatahub.io`
- **User Workload Monitoring**: must be enabled in `openshift-monitoring/cluster-monitoring-config` ConfigMap (`enableUserWorkload: true`) for Prometheus to scrape TrustyAI metrics

## Pod Selectors

- TrustyAI service pods: `app.kubernetes.io/name=trustyai-service`
- Metrics endpoint: `/q/metrics` (Quarkus-style)

## Prometheus Metric Names and Labels

### Bias Metrics

| Metric | Labels | Description |
|--------|--------|-------------|
| `trustyai_spd` | `model`, `protected`, `outcome`, `privileged`, `unprivileged` | Statistical Parity Difference |
| `trustyai_dir` | `model`, `protected`, `outcome`, `privileged`, `unprivileged` | Disparate Impact Ratio |

### Drift Metrics

| Metric | Labels | Description |
|--------|--------|-------------|
| `trustyai_meanshift` | `model`, `feature` | Mean shift detection |
| `trustyai_fouriermmd` | `model`, `feature` | Fourier MMD distribution comparison |
| `trustyai_kstest` | `model`, `feature` | Kolmogorov-Smirnov test statistic |
| `trustyai_jensenshannon` | `model`, `feature` | Jensen-Shannon divergence |

## Recommended Thresholds

| Metric | Fair Value | Default Threshold | Alert When |
|--------|-----------|-------------------|------------|
| SPD | 0 | ±0.1 | \|SPD\| > 0.1 |
| DIR | 1.0 | 0.8–1.2 | DIR < 0.8 or DIR > 1.2 |
| MeanShift | 0 | 0.1 | value > 0.1 |
| FourierMMD | 0 | 0.05 | value > 0.05 |
| KS-Test | 1.0 (p-value) | 0.05 | p-value < 0.05 |
| Jensen-Shannon | 0 | 0.1 | value > 0.1 |

## Minimum Data Requirements

- TrustyAI requires **~100 inference requests** with the protected attribute for stable bias metric computation
- Drift metrics require a **reference dataset** (training data baseline) tagged with `TRAINING` in TrustyAI storage
- Metrics will return NaN or "insufficient data" until the minimum sample size is reached
