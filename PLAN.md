# Modification 6 — `ruff.toml`

Single step (one commit).

## Step 1 — `ruff.toml`

Create `ruff.toml` at the project root:
- `target-version = "py313"`.
- `line-length = 100`.
- `src = ["src"]` — src-layout awareness for import sorting (isort).
- `[lint] select`: `E`, `W` (pycodestyle), `F` (Pyflakes), `I` (isort),
  `N` (naming conventions), `UP` (pyupgrade), `B` (bugbear).

No `[lint] ignore` entries yet — add only if specific rules cause problems.
No auto-fix in config — developers run `ruff format .` manually (see AGENTS.md).

`tox` not yet set up; skip quality gate for this step.
