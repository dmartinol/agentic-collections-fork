# A/B Evaluation Report: rh-virt-vm-lifecycle-manager

## Summary

* Related PR: https://github.com/RHEcosystemAppEng/skill-submissions/pull/18
* LLM: Claude Sonnet 4.5 (vertex_ai)

| Metric | Treatment | Control |
|--------|-----------|---------|
| Trials | 3 | 3 |
| Passed | 3 | 3 |
| Failed | 0 | 0 |
| Errors | 0 | 0 |
| Pass Rate | 1.0000 | 1.0000 |
| Mean Reward | 0.9583 | 0.8750 |
| Median Reward | 1.0000 | 0.8750 |
| Std Reward | 0.0722 | 0.0000 |

## Comparison

- **Mean reward gap (Uplift):** +0.0833
- **Welch's t-test p-value:** 0.1835
- **Fisher's exact p-value:** 1.0000
- **Recommendation:** **PASS**

## Provenance

- Generated at: 2026-05-06T01:28:40.295972+00:00
- Commit SHA: `d42e5977ac8faa772a57f58b7e2eab13d3efd5dd`
- Pipeline run: `abevalflow-9jcpc`
- Treatment image: `image-registry.openshift-image-registry.svc:5000/ab-eval-flow/rh-virt-vm-lifecycle-manager@sha256:912c250eb85bf2f195438880c3edb46a1f37d48908c85cb98b5f0fdb2bd41e87`
- Control image: `image-registry.openshift-image-registry.svc:5000/ab-eval-flow/rh-virt-vm-lifecycle-manager@sha256:8f7a7303d51c6281146e1a2ea4bb2b8ac276b8582657b3038b03f956b17d8ec2`
- Harbor fork revision: `main`

## Trial Details

<details>
<summary>Treatment (3 trials)</summary>

| # | Trial | Reward | Passed |
|---|-------|--------|--------|
| 1 | rh-virt-vm-lifecycle-manager__6UKxKck | 1.0000 | PASS |
| 2 | rh-virt-vm-lifecycle-manager__d88h8AX | 1.0000 | PASS |
| 3 | rh-virt-vm-lifecycle-manager__r5AVgtg | 0.8750 | PASS |

</details>

<details>
<summary>Control (3 trials)</summary>

| # | Trial | Reward | Passed |
|---|-------|--------|--------|
| 1 | rh-virt-vm-lifecycle-manager__kddXkXB | 0.8750 | PASS |
| 2 | rh-virt-vm-lifecycle-manager__tbewTSZ | 0.8750 | PASS |
| 3 | rh-virt-vm-lifecycle-manager__zKnJ778 | 0.8750 | PASS |

</details>
