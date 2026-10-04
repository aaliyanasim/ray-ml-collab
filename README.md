# ray-ml-collab

Git-based collaboration for an ML project (MLOps Assignment 01).
The **ray** team builds a reproducible **financial fraud detection** pipeline while practising a
`dev → staging → main` Git + DVC workflow with reviewed pull requests, CI and a tagged release.

## Team & roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| Aaliyan | Platform owner | CI, pre-commit, environment, releases |
| Yahya | Data owner | DVC, data checks, dataset updates |
| Rehan | Model owner | Training pipeline, configs, experiments |

Everyone writes code and reviews teammates' pull requests.

## Dataset

- **Financial Fraud Detection Dataset** — tabular binary classification (fraud / not fraud).
- Source: [Financial Transactions Dataset for Fraud Detection](https://www.kaggle.com/datasets/aryan208/financial-transactions-dataset-for-fraud-detection)
  by aryan208 on Kaggle.
- The full file (`financial_fraud_detection_dataset.csv`, ~759 MB, 5,000,000 rows, 18 columns,
  fraud rate 3.59%) is too large for the ~50 MB guidance, so the canonical DVC-tracked dataset is a
  fixed **300,000-row stratified sample** (seed 42, fraud rate preserved, ~45.5 MB) at
  `data/raw/financial_fraud_detection_dataset.csv`. Fetch it with `dvc pull`.
- To regenerate the sample from the full download (byte-identical output for the same input):

  ```bash
  uv run python src/make_sample.py --raw-data <path/to/full.csv> \
      --out data/raw/financial_fraud_detection_dataset.csv
  ```

## Branching model

Work flows one way: short-lived branches (`feat/*`, `data/*`, `exp/*`, `fix/*`) → `dev` →
`staging` → `main`. See `CONTRIBUTING.md` for branch naming, the commit convention, the
squash-merge decision and the PR review checklist.

## Project structure

```
configs/            # parameters and pipeline configs
data/               # ignored by Git, tracked by DVC
models/             # ignored by Git, tracked by DVC
notebooks/          # EDA and exploration (jupytext-paired)
src/                # reusable, tested code
tests/              # unit tests
.github/workflows/  # CI
```

## Getting started

```bash
git clone https://github.com/aaliyanasim/ray-ml-collab
cd ray-ml-collab
uv sync          # or: pip install -r requirements.txt
pre-commit install
dvc pull         # fetch data/model artifacts
```
