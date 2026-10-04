# REPORT - ray-ml-collab

## 1. Team, roles and dataset
| Member | GitHub | Role |
|---|---|---|
| Aaliyan | aaliyanasim | Platform owner (CI, pre-commit, environment, releases) |
| Yahya | yahyamobeen | Data owner (DVC, dataset updates) |
| Rehan | Rehan00122 | Model owner (training pipeline, configs, experiments) |

- Repository: https://github.com/aaliyanasim/ray-ml-collab
- Dataset: Financial Fraud Detection Dataset (tabular, binary target `is_fraud`). The raw file (~760 MB, 5M rows) was reduced by `src/make_sample.py` to a fixed stratified sample (~47 MB, 300k rows) tracked with DVC on DagsHub. Source link: see README.
- Leakage: `fraud_type` is only populated on fraud rows, so it is dropped in `src/prepare.py`.

## 2. Reproducibility
| Item | Value |
|---|---|
| Seed | 42 (`params.yaml`) |
| Split | 80/20 stratified |
| Data hash (`.dvc`) | md5 `8306790a952b39ee5b82348fd20af0d3` |
| Environment | `pyproject.toml` + `uv.lock` |
| Pipeline | `dvc.yaml`: prepare -> train -> evaluate (`metrics.json`) |
| Final params | n_estimators 200, max_depth 8, class_weight balanced_subsample |

## 3. Experiments (`exp/` branches)
Fraud rate is 3.6%, so accuracy is misleading; compare F1 and ROC-AUC.

| Run | Params | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|---|
| baseline | depth none, no class weight | 0.964 | 0.000 | 0.000 | 0.000 | 0.577 |
| exp2 `exp/rehan-depth12` (abandoned) | depth 12, balanced_subsample | 0.373 | 0.044 | 0.789 | 0.083 | 0.581 |
| exp3 (promoted, PR #14) | depth 8, 200 trees, balanced_subsample | 0.254 | 0.044 | 0.943 | 0.083 | 0.582 |

Why exp3 won: highest ROC-AUC and recall with equal F1. The baseline never predicted fraud. Overall signal is weak (AUC ~0.58), which suggests the dataset is largely synthetic.

Abandoned branch: `exp/rehan-depth12` is kept unmerged. Depth 12 gave lower recall and AUC than depth 8 / 200 trees, so it was not promoted.

## 4. Pull requests
| PR | Title | Author | State |
|---|---|---|---|
| #1 | docs: add contributing guidelines | aaliyanasim | Closed (superseded by #2) |
| #2 | Chore/cleanup and plan | aaliyanasim | Merged |
| #3 | feat: scaffold reproducible training pipeline | Rehan00122 | Merged |
| #4 | chore: sync dev with main | Rehan00122 | Merged |
| #5 | chore: pin environment with uv | aaliyanasim | Merged |
| #6 | chore: add pre-commit guard rails | aaliyanasim | Merged |
| #7 | style: apply ruff formatting | aaliyanasim | Merged |
| #8 | Feat/ci | aaliyanasim | Merged |
| #9 | DO NOT MERGE - Phase 8 red-check proof | aaliyanasim | Closed (red check demo) |
| #10 | chore: add pull request template | aaliyanasim | Merged |
| #11 | data: track raw dataset sample with DVC | yahyamobeen | Merged |
| #12 | feat: EDA notebook + bucket_hour | Rehan00122 | Merged |
| #13 | fix: declare numpy dependency | aaliyanasim | Merged |
| #14 | feat: class_weight param, promote best experiment | Rehan00122 | Open |

## 5. Retrospective: what broke
- PR #8 CI failed on lint because PR #7 (formatting) had not merged yet; fixed by merging #7 first and updating the branch.
- PR #12 failed lint on a long notebook line; ruff lints `.ipynb` files too.
- Missing dependencies (`pyyaml`, `numpy`) were only caught once CI installed from `uv.lock` (PR #13).
- `dvc pull` first appeared to fail ("file missing"); the cause was that the DagsHub repo is private and credentials were not configured locally. Fixed with `dvc remote modify --local`.
- `.gitignore` initially ignored whole `data/` and `models/` folders, which would have hidden DVC pointers; fixed in PR #2.
- Added to CONTRIBUTING.md: squash-merge policy, branch protection note, PR review checklist.

## 6. Contributions
- Aaliyan: environment pinning, pre-commit guard rails, CI workflow, PR template, ruff formatting.
- Yahya: DVC setup, DagsHub remote, sampled dataset tracking.
- Rehan: training pipeline (prepare/train/evaluate), `params.yaml`/`dvc.yaml`, EDA notebook, feature helper, experiments and promotion.

## 7. Release
Tag `model-v1.0` on `main` after `dev -> staging -> main` release PRs (pending).
