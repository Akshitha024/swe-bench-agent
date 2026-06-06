"""Synthetic SWE-Bench-Lite-shaped instances.

We synthesize 30 instances across 3 fictional repos. Each instance has:
- a small in-memory file map (file_path -> code text)
- a failing test snippet
- the buggy token + correct token (the agent must find and replace).
"""

from __future__ import annotations

import random

from sba.types import Instance

_REPOS = ["acme-utils", "globex-api", "initech-cli"]


def synthesize(n: int = 30, seed: int = 17) -> list[Instance]:
    rng = random.Random(seed)
    out: list[Instance] = []
    for i in range(n):
        repo = _REPOS[i % len(_REPOS)]
        # Two-file mini-codebase. Both files contain the bug token in only one place.
        n_files = rng.randint(2, 4)
        bug = f"BUG_{i:03d}"
        fix = f"FIX_{i:03d}"
        files = {}
        for j in range(n_files):
            files[f"{repo}/src/mod_{j}.py"] = (
                f"def f_{j}(x):\n    return x + {bug if j == 0 else '0'}\n"
            )
        out.append(
            Instance(
                iid=f"inst-{i:03d}",
                repo=repo,
                files=files,
                failing_test=f"assert f_0(1) == 1 + {fix}",
                bug_token=bug,
                fix_token=fix,
            )
        )
    return out
