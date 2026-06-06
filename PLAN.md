# Modification 10 — `src/bgg_search/__init__.py`

Single step (one commit).

## Step 1 — `src/bgg_search/__init__.py`

Create the minimal package entry point:
- Expose `__version__` via `importlib.metadata.version("bgg-search")`.
- No other exports yet — public API surface is built up in phases 0.2–0.4.

`tox` not yet runnable (no lock files); skip quality gate for this step.
