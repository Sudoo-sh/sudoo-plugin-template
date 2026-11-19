# Sudoo.sh plugin template

[![CI](https://github.com/Sudoo-sh/sudoo-plugin-template/actions/workflows/ci.yml/badge.svg)](https://github.com/Sudoo-sh/sudoo-plugin-template/actions/workflows/ci.yml)
[![Release](https://github.com/Sudoo-sh/sudoo-plugin-template/actions/workflows/release.yml/badge.svg)](https://github.com/Sudoo-sh/sudoo-plugin-template/actions/workflows/release.yml)
[![Licence: MIT-0](https://img.shields.io/badge/licence-MIT--0-informational)](LICENSE.md)
[![Sudoo.sh plugin](https://img.shields.io/badge/Sudoo.sh-plugin-714b67)](https://developers.sudoo.sh)

Start a plugin for [Sudoo.sh](https://sudoo.sh), the self-hosted panel that runs a live Odoo for every Git branch on
your own server. Click **Use this template**, rename a few things, and you have a repository that validates, tests
and packs your plugin on every push, and publishes it to the Sudoo.sh marketplace when you push a version tag.

It is built on the [Sudoo.sh plugin SDK](https://github.com/Sudoo-sh/sudoo-plugin-sdk) and holds two working
examples:

| Folder | Plugin | Shows |
| :--- | :--- | :--- |
| [`plugin/`](plugin) | **Midnight** (`com.example.midnight-theme`), a theme | A complete theme: light and dark tokens in the panel's names, a logo, an e-mail accent, tests. This is the plugin the release workflow publishes. |
| [`examples/notification-channel/`](examples/notification-channel) | **Webhook alerts** (`com.example.webhook-alerts`) | A plugin with Python code behind an entry point (`sudoo.notifications`), settings (a secret, two choices), a permission (`network.outbound`) and tests against the SDK's fake panel. |

## Contents

1. [Use this template](#use-this-template)
2. [Renaming checklist](#renaming-checklist)
3. [The SDK dependency](#the-sdk-dependency)
4. [Develop and test locally](#develop-and-test-locally)
5. [Writing your plugin](#writing-your-plugin)
6. [CI](#ci)
7. [Releasing and publishing](#releasing-and-publishing)
8. [The review](#the-review)
9. [Paid plugins](#paid-plugins)
10. [Licence](#licence)
11. [Links](#links)

---

## Use this template

1. On GitHub, click **Use this template**, then **Create a new repository**. Any owner and name work; public or
   private.
2. Clone it and go through the [renaming checklist](#renaming-checklist).
3. Check everything still passes, and commit the updated `plugin/uv.lock`:
   `cd plugin && uv lock && uv sync && uv run sudoo-plugin validate && uv run sudoo-plugin test`.
4. Register as a developer on [developers.sudoo.sh](https://developers.sudoo.sh), and add your developer token to
   the repository as the `SUDOO_DEVELOPER_TOKEN` secret (Settings, Secrets and variables, Actions).
5. Push a tag `v0.1.0` to publish the first version.

## Renaming checklist

Keep `plugin/` as the folder of your plugin (the workflows build that folder), and rename inside it:

- [ ] **Plugin id** in `plugin/manifest.json`: `com.example.midnight-theme` becomes a reverse domain you control,
      for example `com.acme.brand-theme`. It never changes after the first release.
- [ ] **Python package**: rename `plugin/src/example_midnight_theme/` (for example to `acme_brand_theme`), and
      the same name in `pyproject.toml` (`module-name`, `known-first-party`) and in the tests' imports.
- [ ] **Entry point**, the same in both files:
      `manifest.json` → `entry_points` and `pyproject.toml` → `[project.entry-points."sudoo.themes"]`
      (`validate` refuses them when they differ). For another kind of plugin, change `type` and the group:
      `sudoo-plugin types` lists them, and `sudoo-plugin new <type> <id>` writes a starting class for any type.
- [ ] **Class**: `Midnight` in `plugin.py`, and its `label`.
- [ ] **Manifest**: `name`, `description` (10 to 300 characters, shown on the marketplace), `author`, `tags`,
      `homepage` and `issues` (https), `icon`, `license`, `version` (start at `0.1.0`).
- [ ] **pyproject.toml**: `name` (`sudoo-plugin-<your-name>`), `description`, `version` (the same as the
      manifest's).
- [ ] **README.md** in `plugin/`: what your plugin does, its settings and permissions, for the people who install
      it (the marketplace shows it). This file, at the root, is the template's guide: replace it with your own.
- [ ] **CHANGELOG.md** in `plugin/`: one `## <version>` section per release (the release notes and the hub's
      "what changed" come from it).
- [ ] **LICENSE.md** in `plugin/` and at the root: your name, or another licence (and the manifest's `license`).
- [ ] **Badges** at the top of your README: replace `Sudoo-sh/sudoo-plugin-template` with your repository.
- [ ] **Examples**: delete `examples/` when you no longer need it, and remove it from the `matrix` in
      `.github/workflows/ci.yml`.

## The SDK dependency

Each plugin's `pyproject.toml` depends on the SDK from [PyPI](https://pypi.org/project/sudoo-plugin-sdk/):

```toml
[project]
dependencies = ["sudoo-plugin-sdk>=0.1.0,<1.0.0"]
```

The SDK is published on PyPI, so `uv sync` installs it from there. To use the `sudoo-plugin` command outside a
plugin's project, install it on its own:

```bash
pip install sudoo-plugin-sdk          # or: pipx install "sudoo-plugin-sdk[test]"
```

**With a local checkout of the SDK** (to try SDK changes before they are released), either run the
command from the SDK checkout without installing the plugin's project:

```bash
cd plugin
uv run --no-project --with-editable "../../sudoo-plugin-sdk[test]" sudoo-plugin validate
uv run --no-project --with-editable "../../sudoo-plugin-sdk[test]" sudoo-plugin test
uv run --no-project --with-editable "../../sudoo-plugin-sdk[test]" sudoo-plugin pack
```

or point the source at the folder while you work (do not commit it):

```toml
[tool.uv.sources]
sudoo-plugin-sdk = { path = "../../sudoo-plugin-sdk", editable = true }
```

`sudoo-plugin` reads the plugin from `src/`, so validating, testing and packing never need the plugin installed.

`plugin/uv.lock` pins the SDK and the tools, with their hashes, and both workflows install with `uv sync --locked`,
so CI and releases run exactly the locked versions. After changing `pyproject.toml` (the renaming checklist
included), run `uv lock` and commit `uv.lock`; `uv lock --upgrade` moves to newer versions.

## Develop and test locally

You need [uv](https://docs.astral.sh/uv/); it installs Python 3.14 (`.python-version`) by itself.

```bash
cd plugin
uv sync                              # the SDK, pytest, ruff, black, mypy
uv run sudoo-plugin validate         # the hub's automated checks, locally
uv run sudoo-plugin test             # tests/ against the SDK's fake panel
uv run sudoo-plugin pack             # dist/<id>-<version>.sudoo and its SHA-256
uv run ruff check . && uv run black --check . && uv run mypy
uv run sudoo-plugin publish --dry-run   # what a release would send to the hub
```

`pack` is reproducible: the same sources give the same bytes, so the SHA-256 printed here is the one the hub will
list for that version.

## Writing your plugin

**A theme** (this template's `plugin/`) is data: `tokens.css` sets the panel's own custom properties for light and
dark, `logo.svg` is the mark shown next to the product name, and `email_accent` colours the panel's e-mails. The
SDK checks the token names (colours, type faces, radii, shadows and materials only; spacing, sizes and motion stay
the panel's), the light and dark rules, the contrast of text and accent (WCAG AA), and that the logo has no scripts
or outside references. A theme asks for no permission. The SDK README's
[theme guide](https://github.com/Sudoo-sh/sudoo-plugin-sdk#themes) lists every token.

**Any other plugin** is a class behind an entry point, created by the panel with a `PluginContext` (settings,
services, logger, data folder) and called through its group's interface. `examples/notification-channel` is a
complete one: it refuses bad settings at start with a sentence naming the setting, never follows redirects, and
its tests replace the network call so nothing leaves the machine. Run its checks the same way:

```bash
cd examples/notification-channel
uv sync && uv run sudoo-plugin validate && uv run sudoo-plugin test
```

Groups the panel loads today: exposure, add-on sources, update triggers, storage, authenticators, second factors,
mailers, rate limiters. Groups planned for Sudoo.sh 2.0 (their interfaces may still change, and `validate` says
so): backups, notifications, instance hooks, dashboard widgets, web pages, background tasks, themes, API access,
MCP and extensions. Themes and other plugins are installed through the plugin manager of Sudoo.sh 2.0, so
`min_sudoo_version` is `2.0.0`.

## CI

[`ci.yml`](.github/workflows/ci.yml) runs on every push to `main` and every pull request, for each folder in its
matrix: install, ruff, black, mypy, `sudoo-plugin validate`, `sudoo-plugin test`, `sudoo-plugin pack`, and keeps
the `.sudoo` file as a build artifact for 14 days.

## Releasing and publishing

[`release.yml`](.github/workflows/release.yml) runs when you push a tag `v*`:

```bash
# after updating "version" in plugin/manifest.json and plugin/pyproject.toml, and a "## 0.2.0" section in CHANGELOG.md
git tag v0.2.0
git push origin v0.2.0
```

1. Checks that the tag is `v` + the manifest's version.
2. Validates, tests and packs `plugin/`, and writes `SHA256SUMS`.
3. **Publishes to the Sudoo.sh hub** when the `SUDOO_DEVELOPER_TOKEN` secret is set: `sudoo-plugin publish`
   uploads the package, the manifest and this version's changelog section to the developer endpoint that
   developers.sudoo.sh uses (a new plugin the first time, a new version afterwards), and prints the automated
   checks. Without the secret this step is skipped with a notice. The secret is passed to this step only, never
   to the steps that install, validate, test or pack.
4. Creates a GitHub release for the tag with the `.sudoo` file and `SHA256SUMS` attached, and the changelog
   section as its notes.

| Secret | Needed for | Where it comes from |
| :--- | :--- | :--- |
| `SUDOO_DEVELOPER_TOKEN` | Publishing to the hub | Your developer account on developers.sudoo.sh |

The marketplace never builds from your repository: it receives the packed `.sudoo` file, so the review covers
exactly what people install.

## The review

Every version of every plugin goes through the same steps on hub.sudoo.sh; only published versions are listed,
downloadable or installable.

```
submitted ─> automated checks ─┬─> awaiting review ─> approved (signed) ─> published
                               │         │
                               └─────────┴─> changes requested ─(resubmit the same version)─> submitted
```

| Step | What happens |
| :--- | :--- |
| Automated checks | Seconds after upload: manifest schema, `requires`, package structure and size, file paths, forbidden files (keys, `.env`, repository data; compiled files are flagged), permissions against entry points, a static scan, the licence field. `sudoo-plugin validate` runs the same checks before you upload. A failure sends the version back with the report. |
| Test install | A reviewer installs the package on a disposable review panel with sample Odoo data, exercises its settings, then uninstalls it. |
| Human review | Does what the listing says; asks only for the permissions it needs; sends no data off the server without saying so; works in light and dark; has documentation and a working support contact. |
| Publish | The hub signs the package with its Ed25519 key and lists it on marketplace.sudoo.sh. Panels refuse packages that are unsigned or changed. |

Free plugins from verified publishers may skip the human review for patch versions when every automated check
passes; minor and major versions are always reviewed, and paid plugins always are. A published version can be
withdrawn; installed copies keep working without updates. Follow each version's state, checks and the reviewer's
messages on developers.sudoo.sh.

**Publisher badges.** *Official* marks Sudoo.sh's own plugins. *Verified* means Sudoo.sh confirmed who the
publisher is (company registration or ID, a verified domain or e-mail, a signed developer agreement), that their
support channel works, and that they have at least one reviewed plugin; it can be taken back, and renaming the
organisation removes it until it is checked again. Search and featured lists favour verified publishers.

## Paid plugins

Set `"tier": "paid"` and a `"price"` in cents (the first monthly plan) in the manifest. Paid plugins can be
submitted once your developer account is **verified** and your **Stripe Connect** account is set up from
developers.sudoo.sh; Stripe pays your share (70%) to it directly.

| Plan | Billing | Ends |
| :--- | :--- | :--- |
| Monthly | Stripe subscription, renews automatically | End of the paid month |
| Yearly | Stripe subscription, renews automatically | End of the paid year |
| Fixed term | One payment (for example 3 months) | On a fixed date, unless bought again |

- A licence belongs to **one plugin on one panel**. Buyers first link their panel to their account on
  app.sudoo.sh; free plugins never need this.
- Before the end, the account owner and the panel's super admins are reminded. After it, a **grace period**
  (7 days by default) follows; then the panel backs up what the plugin touches and **switches the plugin off,
  keeping its data and settings**. Renewing switches it back on. Nothing is deleted on expiry.
- A panel that cannot reach the hub keeps paid plugins until the end of its last signed lease, then does the same.
- Your plugin needs no licence code of its own: the panel enables and disables it.

## Licence

The template is under **MIT No Attribution** ([LICENSE.md](LICENSE.md)): take it, change it, sell what you build,
with no notice to keep. Replace `LICENSE.md` and the `license` field of `manifest.json` and `pyproject.toml` with
your plugin's own licence (any SPDX expression, or `LicenseRef-Proprietary` for a closed paid plugin). The SDK your
plugin imports is Apache-2.0, which is permissive and does not constrain your choice.

## Links

| | |
| :--- | :--- |
| Product | [sudoo.sh](https://sudoo.sh) |
| Plugin SDK | [github.com/Sudoo-sh/sudoo-plugin-sdk](https://github.com/Sudoo-sh/sudoo-plugin-sdk) |
| Developers | [developers.sudoo.sh](https://developers.sudoo.sh) |
| Documentation | [docs.sudoo.sh](https://docs.sudoo.sh) |
| Marketplace | [marketplace.sudoo.sh](https://marketplace.sudoo.sh) |
| Account | [app.sudoo.sh](https://app.sudoo.sh) |
| Hub API | [hub.sudoo.sh](https://hub.sudoo.sh) |
| Status | [status.sudoo.sh](https://status.sudoo.sh) |
| Panel source | [github.com/Sudoo-sh/sudoo.sh](https://github.com/Sudoo-sh/sudoo.sh) |

© 2026 Sudoo.sh
