# Project Plan — `ray-ml-collab`

Git-Based Collaboration for an ML Project (Assignment 01).
This is the team's chronological execution plan. The order is deliberate:

> **Step 0 — Resolve the blockers/cleanup issues first.**
> **Step 1 — Commit `plan.md` and the cleanup.**
> **Step 2 — Execute Phase 2.**
> **Then Phases 3 → 9.**

Work always flows `dev → staging → main` through reviewed PRs (except the one-time initial
push to `main` in Phase 2).

---

## 1. Team, roles and target

| Member | Role | Owns |
|--------|------|------|
| Aaliyan | **Platform owner** | CI, pre-commit, environment, releases |
| Yahya | **Data owner** | DVC, data checks, dataset updates |
| Rehan | **Model owner** | Training pipeline, configs, experiments |

> Everyone codes and reviews. Every member must author commits, open PRs **and** review
> teammates' PRs. Do not commit on each other's behalf.

- **Repository:** `https://github.com/aaliyanasim/ray-ml-collab`
- **Team name:** `ray`
- **Dataset:** ✅ **Financial Fraud Detection Dataset** — tabular binary classification.
  - Raw file: `financial_fraud_detection_dataset.csv`, **759.17 MB / 5,000,000 rows / 18 columns**.
  - Target: `is_fraud`. ⚠️ `fraud_type` is populated only on fraud rows (direct leakage) → drop it;
    review identifier/PII columns (`transaction_id`, `sender_account`, `receiver_account`,
    `ip_address`, `device_hash`, raw `timestamp`).
  - ⚠️ **Size decision required:** the raw file is ~15× the assignment's ~50 MB guidance. Use a
    **fixed, reproducible sample** (documented generator, fixed seed, fraud rate preserved) as the
    canonical DVC-tracked dataset so `dvc pull`, `dvc repro` and CI stay fast.
  - Record the exact source link in `README.md`/`REPORT.md` (credit the source).
- **Submission:** repo link + `REPORT.md` + tag `model-v1.0` on `main` that a stranger can reproduce.

### Branching model (reference — one-way flow)

| Branch | Purpose | From | Into | Protection |
|--------|---------|------|------|------------|
| `main` | Production, released & tagged | `staging` | — | PR only, 1 approval, CI pass |
| `staging` | Release candidate, reproduced & validated | `main` first time, then `dev` | `main` | PR only, 1 approval, CI pass |
| `dev` | Integration of finished work | `main` first time, then — | `staging` | PR only, 1 approval, CI pass |
| `feat/<name>` | Features / pipeline / refactors | `dev` | `dev` | delete after merge |
| `data/<name>` | Dataset updates (DVC) | `dev` | `dev` | delete after merge |
| `exp/<member>-<idea>` | Exploration, never merged directly | `dev` | — | cherry-pick winner into `feat/` |
| `fix/<name>` | Urgent production fix | `main` | `main`, then `dev` | patch tag |

---

## 2. Status snapshot (as of 2026-10-04)

| Phase | Name | Status |
|-------|------|--------|
| 1 | Team and repository setup | ✅ **Essentially done** (re-verify in Step 0) |
| 2 | Scaffold project & import initial code | 🟡 **In progress** — start after Step 1 |
| 3 | Guard rails: pre-commit and secrets | ❌ Not started |
| 4 | Version data with DVC | ❌ Not started |
| 5 | Notebooks done right | ❌ Not started |
| 6 | Reproducible pipeline | ❌ Not started |
| 7 | Experiments and pull requests | ❌ Not started |
| 8 | CI on every pull request | ❌ Not started |
| 9 | Release: dev → staging → main | ❌ Not started |

**What exists in Git today**

- Remote branches: `main`, `staging`, `dev`, and **`docs/contributing`** (off-model, current HEAD).
- `main` history: `Initial commit` → `chore: scaffold oroject structure` → `Update README.md - assigned roles`.
  `docs/contributing` is **1 commit ahead of `main`** (`docs: add contributing guidelines`).
- Tracked files: `.gitignore`, `.pre-commit-config.yaml` (empty), `CONTRIBUTING.md` (draft), `README.md`.
- `configs/ data/ models/ notebooks/ src/ tests/ .github/workflows/` are **empty local folders only**
  (Git does not track empty directories).

---

## 3. STEP 0 — Resolve blockers & cleanup (do this BEFORE committing anything else)

These are the issues found in the audit. Fix them first so we start Phase 2 from a clean base.
Owners are tagged: **[Platform]** Aaliyan · **[Data]** Yahya · **[Model]** Rehan · **[All]**.

### 0.1 Decide the open choices (needs the team)

| # | Decision | **Chosen** | Owner | Recorded in |
|---|----------|-----------|-------|-------------|
| D1 | Dataset + starter code | ✅ **Financial Fraud Detection Dataset** | [All] | `README.md` + `REPORT.md` |
| D2 | Merge strategy for PRs into `dev` | ✅ **Squash merge** | [All] | `CONTRIBUTING.md` |
| D3 | DVC remote | ✅ **DagsHub** | [Data] | `.dvc/config` (no secrets) |
| D4 | Fate of `docs/contributing` | ✅ **PR → merge → delete branch** | [Platform] | GitHub |

> All decisions are locked. D1 remains a hard gate for the instructor notification by the end of
> Phase 1; Phases 4–9 depend on it.

### 0.2 Fix `CONTRIBUTING.md` (rewritten, no longer a draft)

- [x] **[Platform]** Rewrote `CONTRIBUTING.md` with clean (un-escaped) markdown.
- [x] **[Platform]** Stated the merge decision **D2 = squash merge** for PRs into `dev`.
- [x] **[Platform]** Added the PR **review checklist** section (same list used in the PR template, Phase 7).
- [x] **[Platform]** Added a "Branch protection" note (PR only, 1 approval, all CI checks pass).

### 0.3 Reconcile `.gitignore` with DVC (blocks Phase 4 if left as-is)

Root `.gitignore` currently contains `data/` and `models/`, which **ignores the DVC pointer
files** (`*.dvc`) and DVC's own `data/.gitignore`, so DVC-tracked data could never be committed.
- [x] **[Platform]** Replaced the blanket `data/`/`models/` ignores with file-level patterns
      (`data/**/*.csv`, `models/**/*.pkl`, ...) so real data is ignored but `*.dvc` pointers,
      `data/.gitignore` and `.dvc/config` stay trackable. `.env`, `__pycache__/`, `.venv/`,
      `mlruns/` are still ignored.
- [ ] **[Data]** After `dvc add` in Phase 4, let DVC manage `data/.gitignore` and **verify**
      `git status` shows `*.dvc`, `data/.gitignore` and `.dvc/config` as trackable.

### 0.4 Make the directory layout visible in Git

Empty directories are not tracked, so the required structure is invisible in the repo.
- [x] **[Platform]** Added a `.gitkeep` in `configs/ data/ models/ notebooks/ src/ tests/
      .github/workflows/` so the layout is visible in Git.

### 0.5 Verify Phase 1 on GitHub (could not be checked via CLI)

- [ ] **[Platform]** Confirm Yahya and Rehan have **write** access; instructor is a **viewer**.
- [ ] **[Platform]** Confirm branch protection on `main`/`staging`/`dev` (require PR, ≥1 approval,
      block force pushes; "require status checks" gets enabled in Phase 8).
- [ ] **[All]** Prove push access — each member pushes one throwaway branch, then deletes it.

### 0.6 Collaboration hygiene

- [ ] **[Data + Model]** Yahya and Rehan must start authoring their own commits/PRs now — every
      commit so far is Aaliyan's. Individual marks are adjusted from Git history.
- [ ] **[All]** Do **not** rewrite shared history for the `chore: scaffold oroject structure` typo.
      Note it in `REPORT.md`'s retrospective instead.

**Step 0 is done when:** D1–D4 are decided, `CONTRIBUTING.md` is mergeable, `.gitignore` no longer
blocks DVC pointers, `.gitkeep` files exist, and collaborators/protection are confirmed.

---

## 4. STEP 1 — Commit `plan.md` and the cleanup

1. **[Platform]** Create a short-lived branch off `dev` for the cleanup + plan:
   ```bash
   git fetch origin
   git switch -c chore/cleanup-and-plan origin/dev
   ```
2. **[Platform]** Stage the Step 0 file changes plus `plan.md`:
   ```bash
   git add plan.md .gitignore CONTRIBUTING.md configs/ data/ models/ notebooks/ src/ tests/ .github/workflows/
   git commit -m "chore: add project plan and repo cleanup"
   git push -u origin chore/cleanup-and-plan
   ```
3. **[All]** Open a PR `chore/cleanup-and-plan → dev`; **[All]** a teammate reviews and merges it.
   *(The `plan.md` file lands on `dev` first, then flows to `main` in Phase 2's initial import /
   later release — it is not pushed directly to `main`.)*
4. **[Platform]** Delete the branch after merge:
   ```bash
   git push origin --delete chore/cleanup-and-plan
   git branch -d chore/cleanup-and-plan
   ```

**Step 1 is done when:** `plan.md` and the cleanup are on `dev` via a reviewed PR, and the branch is gone.

---

## 5. STEP 2 — Execute Phase 2 (scaffold project & import initial code)

**Goal / checkpoint:** three protected branches exist; `git log` on `main` shows the initial import.

Since `dev` now holds the cleanup, treat `main` as the base for the one-time initial import
(this is the **only** time anyone pushes directly to `main`).

1. **[Platform]** Track the full, standard layout (`.gitkeep`s from Step 0 make it visible):
   ```
   configs/  data/  models/  notebooks/  src/  tests/  .github/workflows/
   .gitignore  .pre-commit-config.yaml  CONTRIBUTING.md  README.md  plan.md
   pyproject.toml + uv.lock   (or requirements.txt pinned)
   ```
2. **[Model]** Import the starter code into `src/` and refactor it to run from the CLI, e.g.
   `python src/train.py`. Remove **every hardcoded absolute path**.
3. **[Platform]** Pin the environment:
   ```bash
   uv init
   uv add scikit-learn pandas ...      # produces uv.lock
   # or: pip freeze > requirements.txt
   ```
4. **[All]** Commit in small, well-described commits and push to `main`. ⚠️ One-time direct push only.
5. **[Platform]** Create and push the long-lived branches (if not already present):
   ```bash
   git checkout -b staging && git push -u origin staging
   git checkout -b dev && git push -u origin dev
   ```
6. **[Platform]** Ensure branch protection for `main`, `staging`, `dev`: require a pull request,
   ≥1 approval, block force pushes ("require status checks" turns on in Phase 8).
7. **[Platform]** Delete the off-model `docs/contributing` branch once its content is merged.
8. **[All]** Verify: `git log --oneline main` shows the initial import; all three permanent
   branches are protected.

---

## 6. Remaining phases (3 → 9)

Legend: **[Platform]** Aaliyan · **[Data]** Yahya · **[Model]** Rehan · **[All]**

### Phase 3 — Guard rails: pre-commit and secrets
**Checkpoint:** committing a 5 MB file or a fake API key is **blocked** (screenshot for report).
1. **[Platform]** `git switch -c feat/pre-commit dev`.
2. **[Platform]** Fill `.pre-commit-config.yaml` with at least: `ruff` (lint + format),
   `nbstripout`, `check-added-large-files --maxkb=1024`, and a secret scanner
   (`detect-secrets` or `gitleaks`).
3. **[All]** Run `pre-commit install` in each clone.
4. **[Platform]** Prove it: attempt a 5 MB file + a fake key, capture screenshots.
5. **[All]** PR into `dev`; a teammate reviews and merges.

### Phase 4 — Version the data with DVC
**Checkpoint:** the CSV is **not** in Git history — only its `.dvc` pointer.
1. **[Data]** `git switch -c data/initial-dataset dev`.
2. **[Data]** `uv add dvc` (plus the extra for the chosen remote), then `dvc init`.
3. **[Data]** `dvc add data/raw/<dataset>.csv` and
   `dvc remote add -d storage <your-remote>` (credentials outside Git).
4. **[Platform+Data]** Re-verify `.gitignore` keeps real data out but tracks
   `<dataset>.csv.dvc`, `data/.gitignore`, `.dvc/config`.
5. **[Data]** `dvc push` **then** `git push -u origin data/initial-dataset`
   (commit message `data: track raw dataset with DVC`).
6. **[All]** PR into `dev`; reviewer freshly clones + `dvc pull` and confirms. Merge.

### Phase 5 — Notebooks done right
**Checkpoint:** the PR diff shows **no cell outputs or execution counts**.
1. **[Model]** `git switch -c feat/eda-notebook dev`.
2. **[Model]** Create `notebooks/01-eda.ipynb`.
3. **[Model]** `jupytext --set-formats ipynb,py:percent notebooks/01-eda.ipynb`, commit **both** files.
4. **[Model]** Move one reusable function into `src/` with a unit test in `tests/`, import it back.
5. **[Model]** Restart kernel, Run All, then open the PR.

### Phase 6 — A reproducible pipeline
**Checkpoint:** a teammate fresh-clones and `dvc pull && dvc repro` gives **identical metrics**.
1. **[Model]** `git switch -c feat/dvc-pipeline dev`.
2. **[Model]** Put every hyperparameter, split ratio and seed in `params.yaml`
   (`seed: 42`, `split.test_size: 0.2`, `train.model/n_estimators/max_depth`).
3. **[Model]** Split code into **prepare / train / evaluate** in `dvc.yaml`; `evaluate` writes
   `metrics.json`.
4. **[Model]** Seed splitting, shuffling, init and sampling; fit preprocessing on the **train split only**.
5. **[Model]** Log the commit SHA every run (MLflow/W&B, or inside `metrics.json`).
6. **[Model]** `dvc repro`; commit `dvc.yaml dvc.lock params.yaml metrics.json`; `dvc push`; `git push`.
7. **[All]** PR into `dev`; reviewer does the fresh-clone reproduction. Merge.

### Phase 7 — Experiments and pull requests
**Checkpoint:** the PR list shows every member as **both author and reviewer**, with at least one
**"changes requested"** review.
1. **[All]** From `dev`, create `exp/<member>-<idea>`; run **≥3 experiments** on committed code:
   `dvc exp run --set-param train.max_depth=10`; compare with `dvc exp show`; paste the table.
2. **[All]** Promote the winner: `dvc exp apply <name>` → new `feat/` branch → PR into `dev` with
   metrics before → after.
3. **[All]** Every PR assigned to a teammate who fills in the checklist and **requests changes at
   least once**; each member authors **≥2 merged PRs** and reviews **≥2**.
4. **[Data]** `data/<change>` PR (dedupe / labels / rows / split) demonstrating `git checkout` +
   `dvc checkout` across versions.
5. **[All]** Resolve a **real conflict** on the same line of `params.yaml`; second author rebases on
   `dev`, resolves and documents it in the PR.
6. **[All]** Keep **≥1 abandoned `exp/` branch** and explain why in `REPORT.md`.
7. **[Platform]** Add `.github/pull_request_template.md`:
   ```markdown
   ## What changed and why

   ## Metrics (before → after)

   ## Review checklist
   - [ ] No data leakage (no target or future information in features)
   - [ ] Splits are fixed; preprocessing fit on training data only
   - [ ] No hardcoded paths; runs on a teammate's machine
   - [ ] Seeds set for shuffling, initialisation and sampling
   - [ ] Metric computed the way the team reports it
   - [ ] dvc push done before git push (if data or models changed)
   - [ ] Notebook restarted and run top to bottom (if notebooks changed)
   - [ ] Style and naming (linter passes)
   ```

### Phase 8 — CI on every pull request
**Checkpoint:** a deliberately broken test causes a **red check that blocks merging**.
1. **[Platform]** `git switch -c feat/ci dev`.
2. **[Platform]** Add `.github/workflows/ci.yml` on PRs into `dev`, `staging`, `main`:
   `ruff check` + `ruff format --check`; `pytest tests/`; data checks (schema/ranges/nulls);
   smoke train on a few hundred rows; **bonus** CML metrics comment.
3. **[All]** PR into `dev`; review and merge.
4. **[Platform]** Make the checks **required** in branch protection on all three branches.
5. **[Platform]** Break a test to prove a red check blocks merging; screenshot failing + passing CI.

### Phase 9 — Release: dev → staging → main
**Checkpoint:** tag **`model-v1.0`** exists on `main` and the independent reproduction succeeded.
1. **[All]** Release PR **`dev → staging`** titled `release: v1.0` (included PRs + final metrics).
2. **[All — someone who did NOT train the model]** In a new folder:
   ```bash
   git clone <repo> && cd <repo> && git checkout staging
   uv sync
   dvc pull
   dvc repro
   ```
   Post `metrics.json` in the PR — must match exactly.
3. **[All]** Merge to `staging`; PR `staging → main`; merge; then:
   ```bash
   git checkout main && git pull
   git tag -a model-v1.0 -m "First production model"
   git push origin model-v1.0
   ```
4. **[Optional bonus]** `fix/` branch → `main`, tag `model-v1.0.1`, merge `main` back into `dev`.
5. **[All]** Retrospective → update `CONTRIBUTING.md`.

---

## 7. Deliverable: `REPORT.md` (must contain)

- [ ] Team members, roles, dataset and starter-code source (with link)
- [ ] Reproducibility table: **commit SHA, `params.yaml` values, data `.dvc` hash, lock file, seed, final metrics**
- [ ] `dvc exp show` comparison of all experiments and why the winner was chosen
- [ ] Links to: data-update PR, conflict-resolution PR, one "changes requested" review, release PRs,
      and the abandoned `exp/` branch
- [ ] Screenshots: blocked large file or secret, a failing CI check, a passing CI check
- [ ] Retrospective: what broke, and what was added to `CONTRIBUTING.md`
- [ ] One paragraph per member describing their own contribution

## 8. Rubric targets (100 pts + 5 bonus)

| Area | Pts | Covered by |
|------|-----|-----------|
| Repo structure & hygiene | 10 | Steps 0–1, Phases 2–3 |
| Branching & protection | 15 | Step 0.5, Phase 2 |
| Pull requests & review | 20 | Phase 7 |
| Data & model versioning | 15 | Phases 4, 6 |
| Notebooks | 5 | Phase 5 |
| Reproducible experiments | 15 | Phases 6–7 |
| CI | 10 | Phase 8 |
| Release & report | 10 | Phase 9 + `REPORT.md` |
| **Bonus** | +5 | CML PR comment **or** `model-v1.0.1` hotfix |
