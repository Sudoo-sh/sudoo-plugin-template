"""Midnight passes every theme check and keeps text readable in both modes."""

from __future__ import annotations

from pathlib import Path

from sudoo_plugin_sdk.manifest import Manifest
from sudoo_plugin_sdk.theme import THEMEABLE_TOKENS, check_logo_svg, contrast, parse_colour

from example_midnight_theme.plugin import Midnight


def test_every_theme_check_passes() -> None:
    """Test: every theme check passes."""
    report = Midnight.check()
    assert report.errors == []
    assert report.warnings == []


def test_only_panel_tokens_are_set() -> None:
    """Test: only panel tokens are set."""
    report = Midnight.check()
    assert set(report.light) <= THEMEABLE_TOKENS
    assert set(report.dark) <= THEMEABLE_TOKENS


def test_dark_is_its_own_palette() -> None:
    """Test: dark is its own palette."""
    report = Midnight.check()
    for token in ("--accent", "--bg", "--surface", "--text"):
        assert report.dark[token] != report.light[token], token


def test_text_reads_well_in_both_modes() -> None:
    """Test: text reads well in both modes."""
    report = Midnight.check()
    for values in (report.light, report.dark):
        text, surface = parse_colour(values["--text"]), parse_colour(values["--surface"])
        assert text is not None and surface is not None
        assert contrast(text, surface) >= 7  # AAA for body text


def test_logo_is_safe_and_is_the_icon(sudoo_manifest: Manifest, sudoo_project: Path) -> None:
    """Test: logo is safe and is the icon."""
    logo = Midnight.logo_svg()
    assert logo is not None and check_logo_svg(logo) == []
    assert sudoo_manifest.icon is not None
    assert (sudoo_project / sudoo_manifest.icon).read_bytes() == logo


def test_a_theme_asks_for_nothing(sudoo_manifest: Manifest) -> None:
    """Test: a theme asks for nothing."""
    assert sudoo_manifest.permissions == []
    assert sudoo_manifest.type == "theme"
