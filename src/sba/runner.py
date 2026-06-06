"""End-to-end runner."""

from __future__ import annotations

import json
from pathlib import Path

from sba.agent.policy import confused_policy, minimal_edit_policy
from sba.tasks.synthetic import synthesize
from sba.types import RunOutcome
from sba.validator.check import validate
from sba.viz.charts import (
    chars_changed_hist,
    edited_files_bar,
    per_instance_strip,
    per_repo_success,
    repo_x_status_heatmap,
)


def run(
    out_dir: Path, n: int = 30, seed: int = 17, policy_name: str = "minimal_edit"
) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = Path("results/figures")
    instances = synthesize(n=n, seed=seed)
    policy = minimal_edit_policy if policy_name == "minimal_edit" else confused_policy
    rows: list[RunOutcome] = []
    for inst in instances:
        patch = policy(inst)
        rows.append(validate(inst, patch))

    per_repo_success(rows, figs / "per_repo_success.png")
    chars_changed_hist(rows, figs / "chars_changed.png")
    edited_files_bar(rows, figs / "edited_files.png")
    per_instance_strip(rows, figs / "per_instance.png")
    repo_x_status_heatmap(rows, figs / "repo_outcome.png")

    n_pass = sum(r.success for r in rows)
    summary: dict[str, object] = {
        "n_instances": len(rows),
        "n_pass": n_pass,
        "pass_rate": n_pass / max(1, len(rows)),
        "policy": policy_name,
        "rows": [r.model_dump() for r in rows],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    return summary
