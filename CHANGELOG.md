# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `search_games(query, client)` and `get_game(game_id, client)` use-case functions.

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
