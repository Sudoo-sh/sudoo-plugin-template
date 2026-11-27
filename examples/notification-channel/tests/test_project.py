"""The project runs on the same Python locally as in CI."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest


def _version(text: str) -> tuple[int, ...]:
    """Turn "3.14" into (3, 14).

    Args:
        text: A version such as "3.14" or "3.12".

    Returns:
        The numbers of the version.
    """
    return tuple(int(part) for part in text.strip().split("."))


def test_python_is_pinned_in_the_project(sudoo_project: Path) -> None:
    """Test: .python-version sits next to pyproject.toml, where uv looks, and suits requires-python.

    uv looks for .python-version only up to the project's own folder, so a copy at the repository's root alone
    does not choose the Python of `uv sync` here.
    """
    pinned = sudoo_project / ".python-version"
    assert pinned.is_file(), "add a .python-version next to pyproject.toml"
    requires = tomllib.loads((sudoo_project / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    floor = requires["requires-python"].removeprefix(">=")
    assert _version(pinned.read_text(encoding="utf-8")) >= _version(floor)


def test_python_is_the_one_ci_uses(sudoo_project: Path) -> None:
    """Test: the project's .python-version is the repository's, which the workflows give to setup-uv."""
    root = next((folder for folder in sudoo_project.parents if (folder / ".git").exists()), None)
    if root is None or not (root / ".python-version").is_file():
        pytest.skip("Not inside a repository with a .python-version at its root.")
    project = (sudoo_project / ".python-version").read_text(encoding="utf-8").strip()
    assert project == (root / ".python-version").read_text(encoding="utf-8").strip()
