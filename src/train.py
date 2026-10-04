"""CLI entry point for training the fraud detection model."""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

TARGET_COLUMN = "is_fraud"
# fraud_type is only populated on fraud rows, so it leaks the target directly.
LEAKY_COLUMNS = ["fraud_type"]


def parse_args():
    parser = argparse.ArgumentParser(description="Train the fraud detection model.")
    parser.add_argument("--data", required=True, type=Path, help="Path to the training CSV.")
    parser.add_argument("--model-out", required=True, type=Path, help="Where to save the trained model.")
    parser.add_argument("--metrics-out", required=True, type=Path, help="Where to save metrics.json.")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=None)
    return parser.parse_args()


def load_features(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(columns=[c for c in LEAKY_COLUMNS if c in df.columns])
    y = df[TARGET_COLUMN]
    # Non-numeric columns (ids, raw timestamps, etc.) need feature engineering
    # before they're safe to train on; keep the scaffold to numeric columns.
    X = df.drop(columns=[TARGET_COLUMN]).select_dtypes(include="number")
    return X, y


def main():
    args = parse_args()

    X, y = load_features(args.data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.seed,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_out)

    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.write_text(json.dumps(metrics, indent=2))

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
