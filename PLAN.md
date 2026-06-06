# Modification 9 — `tox.ini`

Single step (one commit).

## Step 1 — `tox.ini`

Create `tox.ini` at the project root.

`[tox]` section:
- `requires = tox~=4.55.0` — guards against running with an incompatible version.
- `env_list = lint,type,security,unit` — bare `tox` runs these four.

Environments:

| Env        | package    | deps              | command(s)                                    |
|------------|------------|-------------------|-----------------------------------------------|
| `lint`     | `skip`     | `dev.txt`         | `ruff check` + `ruff format --check`          |
| `type`     | `editable` | `dev.txt`         | `mypy src/`                                   |
| `security` | `skip`     | `dev.txt`         | `bandit -c .bandit -r src/`                   |
| `unit`     | `editable` | `unit.txt`        | `pytest tests/unit/`                          |
| `integ`    | `editable` | `integ.txt`       | `pytest tests/integ/`                         |
| `audit`    | `skip`     | `audit.txt`       | `pip-audit -r requirements/runtime.txt`       |
| `lock`     | `skip`     | `uv` (inline)     | `uv pip compile` each `.in` → `.txt`          |

`package = skip` — tool does not need the package installed.
`package = editable` — package installed in editable mode (PEP 660 via hatchling).

The `lock` env compiles all five `.in` files with `--python-version 3.13`.
The `.txt` files do not exist yet; they are generated in modification 12.

`tox` not yet runnable; skip quality gate for this step.
