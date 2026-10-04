"""End-to-end smoke test: prepare -> train -> evaluate on synthetic data."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
PARAMS = REPO_ROOT / "params.yaml"
METRIC_KEYS = {"accuracy", "precision", "recall", "f1", "roc_auc"}


def _run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_pipeline_runs_end_to_end(sample_csv: Path, tmp_path: Path) -> None:
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"
    model = tmp_path / "model.joblib"
    metrics = tmp_path / "metrics.json"

    result = _run(
        "src/prepare.py",
        "--raw-data",
        str(sample_csv),
        "--train-out",
        str(train),
        "--test-out",
        str(test),
        "--params",
        str(PARAMS),
    )
    assert result.returncode == 0, result.stderr

    # prepare must drop leaky and non-numeric columns.
    prepared = pd.read_csv(train)
    assert "fraud_type" not in prepared.columns
    assert "is_fraud" in prepared.columns
    assert prepared.select_dtypes(include="object").empty

    result = _run(
        "src/train.py",
        "--train-data",
        str(train),
        "--model-out",
        str(model),
        "--params",
        str(PARAMS),
    )
    assert result.returncode == 0, result.stderr
    assert model.exists()

    result = _run(
        "src/evaluate.py",
        "--test-data",
        str(test),
        "--model",
        str(model),
        "--metrics-out",
        str(metrics),
    )
    assert result.returncode == 0, result.stderr

    measured = json.loads(metrics.read_text())
    assert set(measured) == METRIC_KEYS
    assert all(0.0 <= value <= 1.0 for value in measured.values())
