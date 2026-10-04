"""Tests for the CI data-quality checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "src" / "data_checks.py"), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def _prepare_split(sample_csv: Path, tmp_path: Path) -> Path:
    train = tmp_path / "train.csv"
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "src" / "prepare.py"),
            "--raw-data",
            str(sample_csv),
            "--train-out",
            str(train),
            "--test-out",
            str(tmp_path / "test.csv"),
            "--params",
            str(REPO_ROOT / "params.yaml"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return train


def test_passes_on_prepared_split(sample_csv: Path, tmp_path: Path) -> None:
    train = _prepare_split(sample_csv, tmp_path)
    result = _run("--data", str(train))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "passed" in result.stdout


def test_flags_leaky_column(tmp_path: Path) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("fraud_type,amount,is_fraud\ncard,1.0,0\nnone,2.0,1\n")
    result = _run("--data", str(bad), "--min-rows", "1")
    assert result.returncode == 1
    assert "fraud_type" in result.stdout


def test_flags_non_binary_target(tmp_path: Path) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("amount,is_fraud\n1.0,0\n2.0,2\n")
    result = _run("--data", str(bad), "--min-rows", "1")
    assert result.returncode == 1
    assert "binary" in result.stdout


def test_flags_negative_amount(tmp_path: Path) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("amount,is_fraud\n1.0,0\n-5.0,1\n")
    result = _run("--data", str(bad), "--min-rows", "1")
    assert result.returncode == 1
    assert "negative" in result.stdout
