# Modification 7 — `mypy.ini`

Single step (one commit).

## Step 1 — `mypy.ini`

Create `mypy.ini` at the project root:
- `python_version = 3.13`.
- `strict = True` — enables the full strict flag bundle (disallow-untyped-defs,
  warn-return-any, no-implicit-reexport, etc.).
- `mypy_path = src` — src-layout: tells mypy where to resolve package imports.

No per-module overrides yet — add only if specific third-party stubs are missing.

`tox` not yet set up; skip quality gate for this step.
