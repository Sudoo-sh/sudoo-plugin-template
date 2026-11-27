# Changelog

Changes to the template itself. Your plugin's own release notes are in `plugin/CHANGELOG.md`, which the release
workflow and the hub read.

## [Unreleased]

### Fixed

- Local runs use the Python that CI uses. uv looks for `.python-version` only up to the plugin's own folder, so the
  copy at the root was never read by `uv sync` in `plugin/` or `examples/notification-channel/`, which then used
  any Python from 3.12 up while CI used 3.14. Each folder now has its own `.python-version` (3.14), and
  `tests/test_project.py` checks that it suits `requires-python` and equals the root's.
- README: the first version of a plugin is submitted on developers.sudoo.sh; a pushed tag publishes the versions
  after it. A developer API token (the `SUDOO_DEVELOPER_TOKEN` secret) sends new versions only, so a first
  `v0.1.0` tag could not publish a new plugin as the README said.

### Added

- README: "Your first plugin in 10 minutes", from the template to a package a Sudoo.sh panel accepts, with every
  command run against SDK 0.1.1 and Sudoo.sh 3.6.0, and the steps that could not be run that way marked.
