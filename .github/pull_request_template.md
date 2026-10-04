## What changed and why

<!-- Link the issue/experiment and summarise the change. -->

## Metrics (before → after)

<!-- Paste the relevant metrics. Use `dvc exp show` output for experiments. -->

## Review checklist

- [ ] No data leakage (no target or future information in features)
- [ ] Splits are fixed; preprocessing fit on training data only
- [ ] No hardcoded paths; runs on a teammate's machine
- [ ] Seeds set for shuffling, initialisation and sampling
- [ ] Metric computed the way the team reports it
- [ ] dvc push done before git push (if data or models changed)
- [ ] Notebook restarted and run top to bottom (if notebooks changed)
- [ ] Style and naming (linter passes)
