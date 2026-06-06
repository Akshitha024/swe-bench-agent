"""End-to-end runner smoke test."""

from __future__ import annotations

from pathlib import Path

from sba.runner import run


def test_runner_minimal_edit(tmp_path: Path) -> None:
    res = run(tmp_path / "out", n=15, seed=1)
    assert res["n_instances"] == 15
    assert res["pass_rate"] == 1.0  # type: ignore[comparison-overlap]


def test_runner_confused_policy(tmp_path: Path) -> None:
    res = run(tmp_path / "out", n=15, seed=1, policy_name="confused")
    assert res["pass_rate"] == 0.0  # type: ignore[comparison-overlap]
