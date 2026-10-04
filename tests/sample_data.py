"""Generate a small, deterministic synthetic stand-in for the fraud dataset.

The real raw file is ~759 MB (behind DVC), which is far too large for unit tests
and CI. This generates a tiny table with the same *shape*: string identifiers,
a few numeric features, a binary target and the leaky ``fraud_type`` column that
is populated only on fraud rows.

Usage:
    python tests/sample_data.py --out data/raw/sample.csv
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd

SEED = 42
DEFAULT_ROWS = 500
DEFAULT_FRAUD_RATE = 0.08


def make_sample(
    rows: int = DEFAULT_ROWS,
    seed: int = SEED,
    fraud_rate: float = DEFAULT_FRAUD_RATE,
) -> pd.DataFrame:
    """Return a reproducible synthetic fraud dataset as a DataFrame."""
    rng = random.Random(seed)
    records = []
    for i in range(rows):
        is_fraud = 1 if rng.random() < fraud_rate else 0
        amount = round(rng.gammavariate(2.0, 50.0), 2)
        if is_fraud:
            # Fraud is usually larger; keep it learnable but not trivial.
            amount = round(amount * 3 + 10, 2)
        records.append(
            {
                "transaction_id": f"txn_{i:06d}",
                "sender_account": f"acct_{rng.randint(0, 10**6):08d}",
                "receiver_account": f"acct_{rng.randint(0, 10**6):08d}",
                "amount": amount,
                "hour": rng.randint(0, 23),
                "device_hash": f"dev_{rng.randint(0, 16**6):06x}",
                "is_fraud": is_fraud,
                "fraud_type": "card_not_present" if is_fraud else None,
            }
        )
    return pd.DataFrame.from_records(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a synthetic sample CSV.")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    make_sample(rows=args.rows, seed=args.seed).to_csv(args.out, index=False)
    print(f"wrote {args.rows} synthetic rows to {args.out}")


if __name__ == "__main__":
    main()
