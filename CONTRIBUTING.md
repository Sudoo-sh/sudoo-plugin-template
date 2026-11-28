# Contributing to the plugin template

Thank you for helping. Open an issue first for anything larger than a small fix, so we can agree on the shape.

## Before you open a pull request

Run the checks in each plugin folder you changed (`plugin/` and `examples/notification-channel/`):

```bash
uv sync
uv run sudoo-plugin validate && uv run sudoo-plugin test
uv run ruff check . && uv run black --check . && uv run mypy
```

Then, from the repository root, `uvx pre-commit run --all-files`. Sign off every commit (`git commit -s`) to
certify the [Developer Certificate of Origin](https://developercertificate.org).

## Documentation rule

Every module, class and public function has a docstring. It says what the code does, what it takes, what it
returns, which errors it raises and any side effect (network calls, files written). Complex private helpers get
one too. Comments explain why the code is written the way it is, not what each line does.

The `interrogate` pre-commit hook fails when docstring coverage drops under 90%. The template is the first code a
plugin author reads, so keep its examples documented as well as the code you would want to copy.
