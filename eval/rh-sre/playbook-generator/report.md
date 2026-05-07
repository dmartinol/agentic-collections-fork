# A/B Evaluation Report: rh-sre-playbook-generator

## Summary

* Related PR: https://github.com/RHEcosystemAppEng/skill-submissions/pull/13
* LLM: Claude Sonnet 4.6 (vertex_ai)

| Metric | Treatment | Control |
|--------|-----------|---------|
| Trials | 3 | 3 |
| Passed | 3 | 3 |
| Failed | 0 | 0 |
| Errors | 0 | 0 |
| Pass Rate | 1.0000 | 1.0000 |
| Mean Reward | 0.9524 | 0.8571 |
| Median Reward | 1.0000 | 0.8571 |
| Std Reward | 0.0825 | 0.1429 |

## Comparison

- **Mean reward gap (Uplift):** +0.0952
- **Welch's t-test p-value:** 0.3868
- **Fisher's exact p-value:** 1.0000
- **Recommendation:** **PASS**

## Provenance

- Generated at: 2026-05-05T21:26:24.096837+00:00
- Commit SHA: `32a38c2af9cb7d857ead73ea44f0cb1affdfe197`
- Pipeline run: `abevalflow-zdg2x`
- Treatment image: `image-registry.openshift-image-registry.svc:5000/ab-eval-flow/rh-sre-playbook-generator@sha256:3233a8c38ebc066542d730f336f99ba2df16c95c87752b5885c4cffc51206406`
- Control image: `image-registry.openshift-image-registry.svc:5000/ab-eval-flow/rh-sre-playbook-generator@sha256:9b6ec4c7cf97285b642146a7f1079dcc85be6249dabf02210bba1023958f2b00`
- Harbor fork revision: `main`

## Trial Details

<details>
<summary>Treatment (3 trials)</summary>

| # | Trial | Reward | Passed |
|---|-------|--------|--------|
| 1 | rh-sre-playbook-generator__9VAiEdr | 1.0000 | PASS |
| 2 | rh-sre-playbook-generator__EwjdgDy | 1.0000 | PASS |
| 3 | rh-sre-playbook-generator__rYC89Ft | 0.8571 | PASS |

</details>

<details>
<summary>Control (3 trials)</summary>

| # | Trial | Reward | Passed |
|---|-------|--------|--------|
| 1 | rh-sre-playbook-generator__73KvcsC | 0.7143 | PASS |
| 2 | rh-sre-playbook-generator__fYvSJJw | 1.0000 | PASS |
| 3 | rh-sre-playbook-generator__tPLrczd | 0.8571 | PASS |

</details>
