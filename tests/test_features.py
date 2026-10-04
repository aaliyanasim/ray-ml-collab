"""Tests for feature-engineering helpers."""

import pandas as pd

from src.features import bucket_hour


def test_bucket_hour_covers_all_24_hours():
    hours = pd.Series(range(24))
    buckets = bucket_hour(hours)
    assert buckets.isin(["night", "morning", "afternoon", "evening"]).all()


def test_bucket_hour_boundaries():
    assert bucket_hour(pd.Series([0])).iloc[0] == "night"
    assert bucket_hour(pd.Series([6])).iloc[0] == "morning"
    assert bucket_hour(pd.Series([12])).iloc[0] == "afternoon"
    assert bucket_hour(pd.Series([18])).iloc[0] == "evening"
    assert bucket_hour(pd.Series([23])).iloc[0] == "evening"
    assert bucket_hour(pd.Series([5])).iloc[0] == "night"


def test_bucket_hour_rejects_out_of_range():
    import pytest

    with pytest.raises(ValueError):
        bucket_hour(pd.Series([24]))
