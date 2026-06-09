# Phase 0.5 — Documentation & token config

Steps toward the `0.5.0` release.

Each step is implemented on a short-lived feature branch following the development
workflow in [AGENTS.md](AGENTS.md).

**Contents:**

- [Step 1 — CHANGELOG.md ToC sync in release script](#step-1--changelogmd-toc-sync-in-release-script)
- [Step 2 — Docstrings on all public symbols](#step-2--docstrings-on-all-public-symbols)
- [Step 3 — Docs publishing](#step-3--docs-publishing)
- [Step 4 — Token config file](#step-4--token-config-file)
- [Step 5 — README updates](#step-5--readme-updates)

---

## Step 1 — CHANGELOG.md ToC sync in release script

- ✓ `scripts/release.py`: extend `update_changelog` to also prepend a new version row to the
  CHANGELOG.md ToC on each release, so the ToC stays in sync without manual edits.

## Step 2 — Docstrings on all public symbols

- ✓ `src/bgg_search/models.py`: docstrings for `GameSummary` and `GameDetails`
  (class-level and field-level).
- ✓ `src/bgg_search/exceptions.py`: docstrings for `BggSearchError`, `BggApiError`,
  `BggNotFoundError`, `BggParseError`.
- ✓ `src/bgg_search/_protocol.py`: docstring for `BggClientProtocol` and its two methods.
- ✓ `src/bgg_search/search.py`: docstrings for `search_games` and `get_game`.

## Step 3 — Docs publishing

- ✓ Framework choice documented in `DECISIONS.md` (ADR).
- ✓ `requirements/docs.in` + `requirements/docs.txt`: new dep group containing `pdoc`.
- ✓ `tox.ini`: add `docs` env (`pdoc bgg_search -o docs/`); extend `lock` env to include
  docs deps.
- ✓ `scripts/gen_cli_ref.py`: capture `bgg-search --help`, `bgg-search search --help`, and
  `bgg-search details --help` output, then write a minimal HTML page for inclusion in the
  docs site.
- ✓ `.github/workflows/pages.yml`: on every `version/*` tag push, install the package and
  pdoc, generate the API docs site and the CLI reference page, then deploy to GitHub Pages.
  (Requires GitHub Pages source set to "GitHub Actions" in repository settings.)

## Step 4 — Token config file

- ✓ `src/bgg_search/cli.py`: add `--token-file <path>` global option; fall back to reading
  the token from `./.bgg-token` in the working directory when neither `--token-file` nor
  `BGG_TOKEN` is supplied. Resolution order: `--token-file` → `BGG_TOKEN` env var →
  `./.bgg-token` → error.
- ✓ `tests/unit/test_cli.py`: extend with unit tests covering all three resolution paths
  and the missing-token error case.
- ✓ `CHANGELOG.md`: entry under `[Unreleased]`.

## Step 5 — README updates

- `README.md`: replace the "Python API reference" and "CLI reference" sections with links
  to the published GitHub Pages docs site (Quickstart examples stay); document the
  `--token-file` option, `./.bgg-token` dotfile, and the full resolution order
  (`--token-file` → `BGG_TOKEN` → `./.bgg-token` → error) in the Installation section.
