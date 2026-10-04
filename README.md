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
- Source: _TODO — add the exact link here and credit it in `REPORT.md`._
- If the raw file is larger than ~50 MB, a fixed, reproducible sample is used so DVC and CI stay fast.

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
