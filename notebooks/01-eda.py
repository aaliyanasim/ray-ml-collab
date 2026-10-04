# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Fraud dataset EDA
#
# **Status:** Phase 4 (DVC + the real dataset) isn't pullable yet — `dvc push` never
# reached the DagsHub remote, so this notebook runs against the same synthetic
# stand-in `tests/sample_data.py` generates for CI. Re-run it against
# `data/raw/financial_fraud_detection_dataset.csv` once `dvc pull` actually works;
# the column names and leakage/PII findings below come from `plan.md`'s dataset
# audit, not from this synthetic data.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from sample_data import make_sample  # noqa: E402

from src.features import bucket_hour  # noqa: E402

df = make_sample(rows=2000, fraud_rate=0.08)
df.head()

# %% [markdown]
# ## Shape and dtypes

# %%
print(f"{df.shape[0]:,} rows x {df.shape[1]} columns")
df.dtypes

# %% [markdown]
# ## Nulls
#
# `fraud_type` should be the only column with nulls — it's populated on fraud
# rows only, which is exactly why it leaks the target and gets dropped in
# `src/prepare.py`.

# %%
df.isna().mean().rename("null_fraction").to_frame()

# %% [markdown]
# ## Class balance

# %%
class_counts = df["is_fraud"].value_counts()
fraud_rate = df["is_fraud"].mean()
print(f"fraud rate: {fraud_rate:.2%}")
class_counts.plot(kind="bar", title="is_fraud counts")
plt.show()

# %% [markdown]
# ## fraud_type leakage, made visible
#
# `fraud_type` is non-null only when `is_fraud` is 1 — a direct view into the
# target. This is why `LEAKY_COLUMNS` in `src/prepare.py` drops it before
# training.

# %%
pd.crosstab(df["is_fraud"], df["fraud_type"].notna(), rownames=["is_fraud"], colnames=["fraud_type is set"])

# %% [markdown]
# ## Transaction amount by class

# %%
df.boxplot(column="amount", by="is_fraud")
plt.suptitle("")
plt.title("amount by is_fraud")
plt.show()

# %% [markdown]
# ## Reusable feature: time-of-day bucket
#
# `hour` on its own is 24 sparse categories. Bucketing it into four periods
# surfaced a pattern worth keeping as a real feature, so it moved into
# `src/features.py::bucket_hour` with its own unit test
# (`tests/test_features.py`) instead of staying notebook-only.

# %%
df["time_of_day"] = bucket_hour(df["hour"])
df.groupby("time_of_day")["is_fraud"].mean().sort_values(ascending=False)

# %% [markdown]
# ## Columns that need engineering or dropping before training
#
# `src/prepare.py` currently keeps numeric columns only, which drops these
# automatically. They're listed here because `plan.md`'s audit flags them as
# PII / high-cardinality identifiers that would need real feature engineering
# (or dropping) before they're safe to use:
# `transaction_id`, `sender_account`, `receiver_account`, `device_hash`.

# %%
df.select_dtypes(exclude="number").columns.tolist()
