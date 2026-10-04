"""Train the fraud detection model on the prepared training split."""

import argparse
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier

TARGET_COLUMN = "is_fraud"


def parse_args():
    parser = argparse.ArgumentParser(description="Train the fraud detection model.")
    parser.add_argument(
        "--train-data", required=True, type=Path, help="Path to the prepared training CSV."
    )
    parser.add_argument(
        "--model-out", required=True, type=Path, help="Where to save the trained model."
    )
    parser.add_argument("--params", type=Path, default=Path("params.yaml"))
    return parser.parse_args()


def main():
    args = parse_args()
    params = yaml.safe_load(args.params.read_text())

    train_df = pd.read_csv(args.train_data)
    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    model = RandomForestClassifier(
        n_estimators=params["train"]["n_estimators"],
        max_depth=params["train"]["max_depth"],
        random_state=params["seed"],
    )
    model.fit(X_train, y_train)

    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_out)


if __name__ == "__main__":
    main()
