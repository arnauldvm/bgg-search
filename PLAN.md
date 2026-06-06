# Modification 5 — `requirements/*.in`

Single step (one commit): all five files belong to the same logical operation.

## Step 1 — `requirements/*.in`

Create the `requirements/` directory with five unpinned spec files:

| File         | Contents                                  |
|--------------|-------------------------------------------|
| `runtime.in` | empty — no runtime deps this phase        |
| `dev.in`     | `tox`, `ruff`, `mypy`, `bandit[toml]`     |
| `unit.in`    | `pytest`                                  |
| `integ.in`   | `pytest`                                  |
| `audit.in`   | `pip-audit`                               |

Locked `.txt` files are generated in modification 12 (`tox -e lock`).

`tox` not yet set up; skip quality gate for this step.
