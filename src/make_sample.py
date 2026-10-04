"""Draw a fixed, stratified sample of the raw fraud dataset so DVC and CI stay fast.

The full source file is ~760 MB / 5M rows, far above the ~50 MB guidance. This keeps the
fraud rate of the full file and is exactly reproducible from the same input and seed.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

TARGET_COLUMN = "is_fraud"


def parse_args():
    parser = argparse.ArgumentParser(description="Create a reproducible stratified sample.")
    parser.add_argument("--raw-data", required=True, type=Path, help="Path to the full raw CSV.")
    parser.add_argument("--out", required=True, type=Path, help="Where to write the sample CSV.")
    parser.add_argument("--n-rows", type=int, default=300_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--chunksize", type=int, default=500_000)
    return parser.parse_args()


def stratified_row_ids(labels: pd.Series, n_rows: int, seed: int) -> np.ndarray:
    """Pick sorted row positions so each class keeps its share of the full dataset."""
    rng = np.random.default_rng(seed)
    frac = n_rows / len(labels)
    groups = labels.groupby(labels).indices
    picked = [
        rng.choice(groups[label], size=round(len(groups[label]) * frac), replace=False)
        for label in sorted(groups)
    ]
    return np.sort(np.concatenate(picked))


def main():
    args = parse_args()

    # Read everything as text so sampled rows keep their raw values byte-for-byte.
    read_opts = {"dtype": str, "keep_default_na": False}
    labels = pd.read_csv(args.raw_data, usecols=[TARGET_COLUMN], **read_opts)[TARGET_COLUMN]
    keep = stratified_row_ids(labels, args.n_rows, args.seed)

    # Stream the full file in chunks; it does not fit comfortably in memory.
    parts, offset = [], 0
    for chunk in pd.read_csv(args.raw_data, chunksize=args.chunksize, **read_opts):
        in_chunk = keep[(keep >= offset) & (keep < offset + len(chunk))] - offset
        parts.append(chunk.iloc[in_chunk])
        offset += len(chunk)
    sample = pd.concat(parts, ignore_index=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(args.out, index=False)

    full_rate = (labels == "True").mean()
    sample_rate = (sample[TARGET_COLUMN] == "True").mean()
    print(f"rows: {len(labels):,} -> {len(sample):,}")
    print(f"fraud rate: {full_rate:.4%} -> {sample_rate:.4%}")


if __name__ == "__main__":
    main()
