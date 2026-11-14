"""Midnight: an indigo theme for the Sudoo.sh panel (sudoo.themes).

A theme is data: the panel reads tokens.css (its own token names, light and dark), shows logo.svg next to the
product name and uses email_accent in the e-mails it sends. Nothing here runs at request time.
"""

from __future__ import annotations

from sudoo_plugin_sdk import Theme


class Midnight(Theme):
    """Cool neutrals and an indigo accent by day; a deep navy panel by night."""

    label = "Midnight"
    tokens = "tokens.css"
    logo = "logo.svg"
    email_accent = "#3d4fb8"
