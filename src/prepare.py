"""Split the raw fraud-detection dataset into seeded train/test CSVs."""

import argparse
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

TARGET_COLUMN = "is_fraud"
# fraud_type is only populated on fraud rows, so it leaks the target directly.
LEAKY_COLUMNS = ["fraud_type"]


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare train/test splits.")
    parser.add_argument("--raw-data", required=True, type=Path, help="Path to the raw CSV.")
    parser.add_argument("--train-out", required=True, type=Path)
    parser.add_argument("--test-out", required=True, type=Path)
    parser.add_argument("--params", type=Path, default=Path("params.yaml"))
    return parser.parse_args()


def main():
    args = parse_args()
    params = yaml.safe_load(args.params.read_text())

    df = pd.read_csv(args.raw_data)
    df = df.drop(columns=[c for c in LEAKY_COLUMNS if c in df.columns])

    # Non-numeric columns (ids, raw timestamps, etc.) need feature engineering
    # before they're safe to train on; keep the scaffold to numeric columns.
    feature_columns = df.select_dtypes(include="number").columns.tolist()
    if TARGET_COLUMN not in feature_columns:
        feature_columns.append(TARGET_COLUMN)
    df = df[feature_columns]

    train_df, test_df = train_test_split(
        df,
        test_size=params["prepare"]["test_size"],
        random_state=params["seed"],
        stratify=df[TARGET_COLUMN],
    )

    args.train_out.parent.mkdir(parents=True, exist_ok=True)
    args.test_out.parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(args.train_out, index=False)
    test_df.to_csv(args.test_out, index=False)


if __name__ == "__main__":
    main()
