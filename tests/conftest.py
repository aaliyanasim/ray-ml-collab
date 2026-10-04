"""Shared pytest fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from sample_data import make_sample  # noqa: E402


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """Path to a freshly generated deterministic synthetic dataset."""
    path = tmp_path / "sample.csv"
    make_sample().to_csv(path, index=False)
    return path
