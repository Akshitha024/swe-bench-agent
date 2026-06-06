"""Types for the SWE-Bench-Lite agent."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Instance(BaseModel):
    """One SWE-Bench-Lite-shaped instance."""

    iid: str
    repo: str
    files: dict[str, str] = Field(default_factory=dict)
    failing_test: str
    bug_token: str = Field(..., description="The exact buggy token to replace.")
    fix_token: str = Field(..., description="The replacement token that fixes the test.")


class Patch(BaseModel):
    """A produced patch."""

    iid: str
    file_path: str
    old: str
    new: str


class RunOutcome(BaseModel):
    iid: str
    repo: str
    success: bool
    edited_files: int
    chars_changed: int
