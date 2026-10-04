"""Data quality checks for the model-input table.

Runs in CI (Phase 8) on the prepared train/test split, and can be wired into the
DVC pipeline as a validation stage later. It checks schema, ranges, nulls and,
most importantly, that no leaky columns reached the model input.

Usage:
    python src/data_checks.py --data data/processed/train.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

TARGET_COLUMN = "is_fraud"
# fraud_type is populated only on fraud rows, so it leaks the target directly.
LEAKY_COLUMNS = ("fraud_type",)
DEFAULT_MIN_ROWS = 50
DEFAULT_MAX_NULL_FRACTION = 0.0


def check_frame(
    df: pd.DataFrame,
    *,
    min_rows: int = DEFAULT_MIN_ROWS,
    max_null_fraction: float = DEFAULT_MAX_NULL_FRACTION,
) -> list[str]:
    """Return a list of human-readable problems (empty means the data is valid)."""
    problems: list[str] = []

    if df.empty:
        return ["dataset is empty"]

    if TARGET_COLUMN not in df.columns:
        problems.append(f"missing target column '{TARGET_COLUMN}'")

    for column in LEAKY_COLUMNS:
        if column in df.columns:
            problems.append(f"leaky column '{column}' must be dropped before training")

    if TARGET_COLUMN in df.columns:
        target = df[TARGET_COLUMN]
        if target.isna().any():
            problems.append("target column contains nulls")
        values = set(target.dropna().unique().tolist())
        if not values <= {0, 1}:
            problems.append(f"target must be binary 0/1, found {sorted(values)}")

    features = df.drop(columns=[TARGET_COLUMN], errors="ignore")
    if features.shape[1] == 0:
        problems.append("no feature columns present")

    null_fraction = features.isna().mean()
    offenders = null_fraction[null_fraction > max_null_fraction]
    if not offenders.empty:
        problems.append(
            f"null fraction exceeds {max_null_fraction:.0%}: {offenders.round(4).to_dict()}"
        )

    if "amount" in features.columns:
        amounts = pd.to_numeric(features["amount"], errors="coerce")
        if amounts.isna().any():
            problems.append("'amount' contains non-numeric values")
        elif (amounts < 0).any():
            problems.append("'amount' contains negative values")

    if len(df) < min_rows:
        problems.append(f"only {len(df)} rows, expected at least {min_rows}")

    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the model-input dataset.")
    parser.add_argument("--data", required=True, type=Path, help="CSV to validate.")
    parser.add_argument("--min-rows", type=int, default=DEFAULT_MIN_ROWS)
    parser.add_argument(
        "--max-null-fraction",
        type=float,
        default=DEFAULT_MAX_NULL_FRACTION,
        help="Allowed fraction of nulls per feature column (0.0 = none).",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    problems = check_frame(df, min_rows=args.min_rows, max_null_fraction=args.max_null_fraction)

    if problems:
        print(f"DATA CHECKS FAILED for {args.data}:")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)

    print(f"data checks passed for {args.data}: {len(df)} rows x {df.shape[1]} columns")


if __name__ == "__main__":
    main()
