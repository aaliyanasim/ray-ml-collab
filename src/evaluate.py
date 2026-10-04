"""Evaluate the trained fraud detection model on the held-out test split."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

TARGET_COLUMN = "is_fraud"


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate the trained model.")
    parser.add_argument(
        "--test-data", required=True, type=Path, help="Path to the prepared test CSV."
    )
    parser.add_argument("--model", required=True, type=Path, help="Path to the trained model.")
    parser.add_argument(
        "--metrics-out", required=True, type=Path, help="Where to save metrics.json."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    test_df = pd.read_csv(args.test_data)
    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    model = joblib.load(args.model)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
