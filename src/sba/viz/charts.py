"""Five chart families for swe-bench-agent."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from sba.types import RunOutcome


def _save(fig: Figure, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def per_repo_success(rows: list[RunOutcome], out: Path) -> Path:
    by_repo: dict[str, list[int]] = {}
    for r in rows:
        by_repo.setdefault(r.repo, []).append(int(r.success))
    repos = sorted(by_repo)
    rates = [sum(by_repo[k]) / len(by_repo[k]) for k in repos]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(repos, rates, color="#3b6fa1")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("success rate")
    ax.set_title("Per-repo success rate")
    for bar, rate in zip(bars, rates, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            rate + 0.02,
            f"{rate:.0%}",
            ha="center",
            fontsize=9,
        )
    return _save(fig, out)


def chars_changed_hist(rows: list[RunOutcome], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist([r.chars_changed for r in rows], bins=20, color="#5b8d4a", edgecolor="white")
    ax.set_xlabel("chars changed")
    ax.set_ylabel("instances")
    ax.set_title("Minimal-edit footprint")
    return _save(fig, out)


def edited_files_bar(rows: list[RunOutcome], out: Path) -> Path:
    cnt = Counter(r.edited_files for r in rows)
    xs = sorted(cnt)
    ys = [cnt[x] for x in xs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([str(x) for x in xs], ys, color="#c25a4f")
    ax.set_xlabel("# files edited")
    ax.set_ylabel("instances")
    ax.set_title("Files edited per instance")
    return _save(fig, out)


def per_instance_strip(rows: list[RunOutcome], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 3))
    xs = np.arange(len(rows))
    colors = ["#5b8d4a" if r.success else "#c25a4f" for r in rows]
    ax.scatter(xs, [1] * len(rows), c=colors, marker="s", s=40)
    ax.set_yticks([])
    ax.set_xlabel("instance index")
    ax.set_title("Per-instance success (green) / failure (red) strip")
    return _save(fig, out)


def repo_x_status_heatmap(rows: list[RunOutcome], out: Path) -> Path:
    repos = sorted({r.repo for r in rows})
    mat = np.zeros((len(repos), 2))
    for r in rows:
        mat[repos.index(r.repo), 0 if r.success else 1] += 1
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(mat, aspect="auto", cmap="viridis")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["pass", "fail"])
    ax.set_yticks(range(len(repos)))
    ax.set_yticklabels(repos)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, str(int(mat[i, j])), ha="center", va="center", color="w", fontsize=10)
    ax.set_title("Repo x outcome")
    fig.colorbar(im, ax=ax)
    return _save(fig, out)
