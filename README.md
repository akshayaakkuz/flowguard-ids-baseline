# FlowGuard IDS Baseline

A compact, dependency-free baseline for detecting anomalous network flows. It is designed for teaching, reproducible experiments, and as a starting point for a real intrusion-detection pipeline.

## What it does

- Generates labeled synthetic network-flow data with benign, scan, exfiltration, and brute-force-like patterns.
- Fits robust per-feature statistics from benign training flows.
- Scores a new flow using a median absolute deviation (MAD) anomaly score.
- Emits a JSON decision with a score, threshold, and human-readable feature contributions.

## Quick start

Requires Python 3.10+ and no third-party packages.

```bash
python -m flowguard.generate_data --output data/flows.csv --rows 1000
python -m flowguard.train --input data/flows.csv --model model.json
python -m flowguard.score --model model.json --input data/flows.csv --limit 10
python -m unittest discover -s tests -v
```

## Data schema

`duration_s`, `bytes_sent`, `bytes_received`, `packets`, `dst_port`, `failed_logins`, `label`

The generator is deliberately synthetic: do not treat its detection quality as evidence of production performance.

## Responsible use

Use FlowGuard only on systems and traffic you are authorized to monitor. This repository is a defensive baseline, not a replacement for validation, privacy review, security operations processes, or human investigation.

## Method

For each numeric feature, FlowGuard learns the benign median and MAD. A flow's feature deviation is `abs(x - median) / (1.4826 * MAD)`. The flow score is the maximum feature deviation; a score at or above the configured threshold is flagged. This makes the baseline transparent and robust to isolated outliers, but it cannot model feature interactions or adapt to concept drift.

## License

MIT. See [LICENSE](LICENSE).
