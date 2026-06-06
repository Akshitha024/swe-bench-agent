"""Tests for the synthetic task generator."""

from __future__ import annotations

from sba.tasks.synthetic import synthesize


def test_count() -> None:
    assert len(synthesize(n=20, seed=1)) == 20


def test_each_instance_has_at_least_two_files() -> None:
    for inst in synthesize(n=30, seed=2):
        assert len(inst.files) >= 2


def test_bug_token_unique_to_one_file() -> None:
    for inst in synthesize(n=20, seed=3):
        n = sum(inst.bug_token in v for v in inst.files.values())
        assert n == 1
