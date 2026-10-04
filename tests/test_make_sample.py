import numpy as np
import pandas as pd

from src.make_sample import stratified_row_ids


def make_labels(n_fraud=50, n_legit=950):
    labels = ["True"] * n_fraud + ["False"] * n_legit
    return pd.Series(np.random.default_rng(0).permutation(labels))


def test_sample_keeps_fraud_rate():
    labels = make_labels()
    rows = stratified_row_ids(labels, n_rows=200, seed=42)
    assert len(rows) == 200
    assert (labels.iloc[rows] == "True").sum() == 10  # 5% of 200


def test_sample_is_reproducible_and_unique():
    labels = make_labels()
    first = stratified_row_ids(labels, n_rows=200, seed=42)
    second = stratified_row_ids(labels, n_rows=200, seed=42)
    assert np.array_equal(first, second)
    assert len(np.unique(first)) == len(first)
    assert np.all(np.diff(first) > 0)  # sorted, so chunked reads can stream in order


def test_different_seed_gives_different_sample():
    labels = make_labels()
    assert not np.array_equal(
        stratified_row_ids(labels, n_rows=200, seed=42),
        stratified_row_ids(labels, n_rows=200, seed=7),
    )
