"""Minimal-edit policy.

  1. Use BM25 to find the most likely file containing the bug.
  2. Locate the bug token in that file.
  3. Replace it with the fix token.
  4. Return a single-file patch.

A 'confused' policy is included that picks the wrong file; used to verify the
validator rejects bad patches.
"""

from __future__ import annotations

from rank_bm25 import BM25Okapi  # type: ignore[import-untyped]

from sba.types import Instance, Patch


def minimal_edit_policy(inst: Instance) -> Patch:
    files = list(inst.files.items())
    # Score each file by BM25 against the failing-test snippet.
    tokenized = [text.lower().split() for _, text in files]
    bm = BM25Okapi(tokenized)
    qtok = inst.failing_test.lower().split()
    scores = bm.get_scores(qtok)
    # Prefer the file that actually contains the bug token.
    best_idx = max(
        range(len(files)),
        key=lambda i: (inst.bug_token in files[i][1], scores[i]),
    )
    fp = files[best_idx][0]
    return Patch(iid=inst.iid, file_path=fp, old=inst.bug_token, new=inst.fix_token)


def confused_policy(inst: Instance) -> Patch:
    """Always edit the first file with a wrong replacement."""
    fp = next(iter(inst.files))
    return Patch(iid=inst.iid, file_path=fp, old="def", new="def_wrong")
