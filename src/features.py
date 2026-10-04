"""Reusable feature-engineering helpers surfaced during EDA."""

import pandas as pd

TIME_OF_DAY_BUCKETS = [
    (0, 6, "night"),
    (6, 12, "morning"),
    (12, 18, "afternoon"),
    (18, 24, "evening"),
]


def bucket_hour(hour: pd.Series) -> pd.Series:
    """Map an hour-of-day column (0-23) to a time-of-day bucket."""

    def label(h):
        for start, end, name in TIME_OF_DAY_BUCKETS:
            if start <= h < end:
                return name
        raise ValueError(f"hour out of range: {h}")

    return hour.apply(label)
