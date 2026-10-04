"""Intentionally failing test used to prove CI blocks merges (Phase 8).

This lives on a throwaway `exp/` branch and must never be merged.
"""


def test_intentionally_broken_for_ci_demo() -> None:
    assert 1 + 1 == 3, "Phase 8 proof: a red check must block merging."
