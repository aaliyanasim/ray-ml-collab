# Contributing

How we work on **ray-ml-collab**. Following this keeps the repository reproducible and the
Git history reviewable.

## One-way branch flow

`feat/*`, `data/*`, `exp/*`, `fix/*` → **dev** → **staging** → **main**.
Nobody pushes directly to `dev`, `staging` or `main` — all changes arrive through reviewed PRs.
(The only exception is the one-time initial import to `main` in Phase 2.)

## Branch naming

| Prefix | Purpose | Branched from | Merged into |
|--------|---------|---------------|-------------|
| `feat/<name>` | Features, pipeline changes, refactors | `dev` | `dev` |
| `data/<name>` | Dataset updates (DVC-tracked) | `dev` | `dev` |
| `exp/<member>-<idea>` | Personal experiments (never merged directly) | `dev` | — |
| `fix/<name>` | Urgent production fixes | `main` | `main`, then `dev` |

Delete short-lived branches after they merge.

## Commit messages (Conventional Commits)

- `feat: ...` — production code changes
- `data: ...` — dataset changes
- `exp: ...` — experiment branches
- `fix: ...` — hotfixes
- `docs: ...` — documentation only
- `chore: ...` — tooling/scaffolding, no logic change

## Merge strategy

**Squash merge** PRs into `dev`. Each PR becomes a single, clean commit on `dev`; the source
branch is deleted after merging. Releases are promoted by merge `dev → staging → main`.

## Branch protection

`main`, `staging` and `dev` are protected:

- Pull request required; no direct pushes
- At least **1 approval**
- All CI checks must pass (enabled in Phase 8)
- Force pushes blocked

## Review checklist

Every PR reviewer pastes this checklist as a comment:

- [ ] No data leakage (no target or future information in features)
- [ ] Splits are fixed; preprocessing fit on training data only
- [ ] No hardcoded paths; runs on a teammate's machine
- [ ] Seeds set for shuffling, initialisation and sampling
- [ ] Metric computed the way the team reports it
- [ ] `dvc push` done before `git push` (if data or models changed)
- [ ] Notebook restarted and run top to bottom (if notebooks changed)
- [ ] Style and naming (linter passes)
