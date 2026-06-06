"""Tests for the minimal-edit + confused policies."""

from __future__ import annotations

from sba.agent.policy import confused_policy, minimal_edit_policy
from sba.tasks.synthetic import synthesize


def test_minimal_edit_picks_file_with_bug() -> None:
    for inst in synthesize(n=20, seed=4):
        patch = minimal_edit_policy(inst)
        assert inst.bug_token in inst.files[patch.file_path]


def test_confused_policy_picks_first_file() -> None:
    inst = synthesize(n=1)[0]
    patch = confused_policy(inst)
    assert patch.file_path == next(iter(inst.files))


def test_minimal_edit_patch_uses_fix_token() -> None:
    inst = synthesize(n=1)[0]
    patch = minimal_edit_policy(inst)
    assert patch.new == inst.fix_token
