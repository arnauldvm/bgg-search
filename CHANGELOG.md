# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Contents:**

- [Unreleased](#unreleased)
- [0.6.0 - 2026-06-10](#060---2026-06-10)
- [0.5.1 - 2026-06-10](#051---2026-06-10)
- [0.5.0 - 2026-06-09](#050---2026-06-09)
- [0.4.0 - 2026-06-08](#040---2026-06-08)
- [0.3.1 - 2026-06-07](#031---2026-06-07)
- [0.3.0 - 2026-06-07](#030---2026-06-07)
- [0.2.0 - 2026-06-07](#020---2026-06-07)
- [0.1.0 - 2026-06-07](#010---2026-06-07)

## [Unreleased]

## [0.6.0 - 2026-06-10]

### Added

- `BggClient` now throttles API calls to at most `requests_per_second` per second
  (default: 2.0); pass `None` to disable.
- `--requests-per-second N` CLI option overrides the throttle (default: 2.0).

## [0.5.1 - 2026-06-10]

### Added

- Dark mode support on the GitHub Pages documentation site.
- Enriched docs landing page with project description, current version, and resource links.
- Version number in the CLI reference page title and heading.

## [0.5.0 - 2026-06-09]

### Added

- Docstrings on all public API symbols (`GameSummary`, `GameDetails`, `BggClientProtocol`,
  `search_games`, `get_game`, exception classes) — visible in IDEs and via `help()`.
- Published API reference (<https://arnauldvm.github.io/bgg-search/api.html>) and CLI reference
  (<https://arnauldvm.github.io/bgg-search/cli.html>) on GitHub Pages, with a landing page at
  the root (<https://arnauldvm.github.io/bgg-search/>).
- `--token-file PATH` global option to supply the BGG API token from a file.
- `.bgg-token` dotfile support: token is read from `./.bgg-token` in the working
  directory as a last resort. Resolution order: `--token-file` → `BGG_TOKEN` → `.bgg-token`.
- `CONTRIBUTING.md` with development setup and test instructions.

## [0.4.0] - 2026-06-08

### Added

- `search_games(query, client)` and `get_game(game_id, client)` use-case functions.
- `bgg-search search <query>` and `bgg-search details <id>` CLI commands.

## [0.3.1] - 2026-06-07

### Added

- Release automation: `tox -e release` / `tox -e release-no-publish` invoke `scripts/release.py`,
  which handles locking, auditing, integration tests, version bumping, changelog update,
  tagging, pushing, and PyPI verification in a single command.

## [0.3.0] - 2026-06-07

### Added

- `BggClient`: concrete `httpx`-based implementation of `BggClientProtocol`, with `search` and
  `get_game` methods. Requires a BGG API token passed via the `token` constructor argument.

## [0.2.0] - 2026-06-07

### Added

- Public API surface: `GameSummary`, `GameDetails`, `BggSearchError`, `BggApiError`,
  `BggNotFoundError`, `BggParseError`, `BggClientProtocol`.

## [0.1.0] - 2026-06-07

### Added

- Initial release of `bgg-search`: a Python client and CLI for the BoardGameGeek XML API.
- Package installable from PyPI; requires Python ≥ 3.13.
- `bgg_search.__version__` exposes the installed package version.
- MIT license.
