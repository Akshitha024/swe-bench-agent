"""Tests for the patch validator."""

from __future__ import annotations

from sba.agent.policy import confused_policy, minimal_edit_policy
from sba.tasks.synthetic import synthesize
from sba.validator.check import validate


def test_minimal_edit_passes_validation() -> None:
    inst = synthesize(n=1)[0]
    patch = minimal_edit_policy(inst)
    out = validate(inst, patch)
    assert out.success


def test_confused_patch_fails_validation() -> None:
    inst = synthesize(n=1)[0]
    patch = confused_policy(inst)
    out = validate(inst, patch)
    assert not out.success
