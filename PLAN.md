# Plan — Docs publishing

## Steps

1. ✓ Compare API doc generation frameworks and document the choice in `DECISIONS.md`.
2. ✓ Framework setup: `requirements/docs.in`, `requirements/docs.txt`, `tox.ini` (add `docs`
   env, extend `lock` env), `.gitignore` (exclude `site/`).
3. CLI reference generator: `scripts/gen_cli_ref.py`; extend the `docs` tox env in
   `tox.ini` to also run it.
4. GitHub Pages workflow: `.github/workflows/pages.yml` — on every `version/*` tag push,
   generate the API docs and CLI reference page, then deploy to GitHub Pages.
