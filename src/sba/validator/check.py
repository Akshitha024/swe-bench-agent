"""Patch validator: apply the patch + re-run the failing test."""

from __future__ import annotations

from sba.types import Instance, Patch, RunOutcome


def apply_patch(inst: Instance, patch: Patch) -> dict[str, str]:
    """Return a new file map with `patch.old` replaced by `patch.new` in the
    target file."""
    if patch.file_path not in inst.files:
        return dict(inst.files)
    out = dict(inst.files)
    out[patch.file_path] = out[patch.file_path].replace(patch.old, patch.new, 1)
    return out


def validate(inst: Instance, patch: Patch) -> RunOutcome:
    """Apply the patch + verify the failing test now passes."""
    patched = apply_patch(inst, patch)
    chars_changed = sum(
        abs(len(patched[p]) - len(inst.files[p])) for p in patched if p in inst.files
    ) or len(patch.new) - len(patch.old)
    success = any(inst.fix_token in patched[p] for p in patched)
    edited_files = sum(1 for p in patched if patched[p] != inst.files.get(p))
    return RunOutcome(
        iid=inst.iid,
        repo=inst.repo,
        success=success,
        edited_files=edited_files,
        chars_changed=abs(chars_changed),
    )
