"""Typer CLI for swe-bench-agent."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from sba.runner import run

app = typer.Typer(no_args_is_help=True, help="SWE-Bench-Lite focused minimal-edit agent.")
console = Console()


@app.command()
def info() -> None:
    console.print("swe-bench-agent: see `sba bench --help`.")


@app.command()
def bench(
    out_dir: Path = typer.Option(Path("runs/latest")),
    n: int = typer.Option(30),
    seed: int = typer.Option(17),
    policy: str = typer.Option("minimal_edit"),
) -> None:
    res = run(out_dir, n=n, seed=seed, policy_name=policy)
    console.print_json(
        json.dumps(
            {k: v for k, v in res.items() if k != "rows"},
            default=str,
        )
    )


if __name__ == "__main__":
    app()
