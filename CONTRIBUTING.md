\# Contributing



\## Branch Naming

\- feat/<name>   — new features, pipeline changes, code

\- data/<name>   — dataset updates (DVC-tracked)

\- exp/<member>-<idea> — personal experiment branches, may never merge

\- fix/<name>    — urgent fixes to production (branched from main)



\## Commit Messages (Conventional Commits)

\- feat: ...   — production code changes

\- data: ...   — dataset changes

\- exp: ...    — experiment branches

\- fix: ...    — hotfixes

\- docs: ...   — documentation only

\- chore: ...  — tooling/scaffolding, no logic change



\## Merge Strategy

We use \[squash merge / rebase merge — pick one] for PRs into dev.



\## Team Roles

\- Data owner: Yahya — DVC, data checks, dataset updates

\- Model owner: Rehan — training pipeline, configs, experiments

\- Platform owner: Aaliyan — CI, pre-commit, environment, releases

