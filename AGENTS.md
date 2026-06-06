# BGG Search — Agent Guide

## Project context

`bgg-search` is a personal Python package for querying [BoardGameGeek](https://boardgamegeek.com) (BGG).
It wraps the BGG XML API2 and exposes:

- a clean, reusable Python API for searching games, retrieving game details, and filtering results;
- a generic CLI for interacting with the BGG API from the command line.

This is a personal project; prioritize clarity and correctness over enterprise-grade robustness.

Rationale behind key choices is documented in [DECISIONS.md](DECISIONS.md).

### Repository layout (target structure)

```
bgg-search/
├── src/
│   └── bgg_search/          # installable package
│       ├── __init__.py      # explicit public API surface
│       ├── models.py        # pure domain dataclasses
│       ├── exceptions.py    # all domain exceptions
│       ├── _protocol.py     # BggClientProtocol (typing.Protocol)
│       ├── _client.py       # concrete httpx client + XML parsing
│       ├── search.py        # use-case layer
│       └── cli.py           # CLI adapter (I/O only)
├── tests/
│   ├── conftest.py
│   ├── unit/                # fast, purely local tests
│   │   ├── conftest.py
│   │   └── test_*.py
│   └── integ/               # slow, hits the real BGG API
│       ├── conftest.py
│       └── test_*.py
├── requirements/
│   ├── runtime.in           # package runtime deps (unpinned spec)
│   ├── runtime.txt          # locked runtime deps
│   ├── dev.in               # tooling: tox, ruff, mypy, bandit (unpinned spec)
│   ├── dev.txt              # locked tooling deps
│   ├── unit.in              # unit test deps (unpinned spec)
│   ├── unit.txt             # locked unit test deps
│   ├── integ.in             # integ test deps (unpinned spec)
│   ├── integ.txt            # locked integ test deps
│   ├── audit.in             # pip-audit (unpinned spec)
│   └── audit.txt            # locked audit deps
├── pyproject.toml           # package metadata and build system only
├── CHANGELOG.md
├── PROCESS.md
├── README.md
└── AGENTS.md
```

## Development environment

Dependencies are managed with **uv**. Each context has its own requirements file (see `requirements/`).
`.in` files are the unpinned specs; `.txt` files are the locked versions generated from them.

```bash
# create and activate a virtual environment
uv venv && source .venv/bin/activate

# install the package in editable mode with locked dev deps
uv pip install -e . -r requirements/dev.txt
```

There is no `setup.py`. `pyproject.toml` contains package metadata and build system only; all dependency declarations live in `requirements/`.

### Commands

All tasks run through **tox**, which executes each step in an isolated virtualenv.

| Task | Command |
|------|---------|
| Full quality gate (lint + type + security + unit tests) | `tox` |
| Lint / format | `tox -e lint` |
| Type-check | `tox -e type` |
| Security scan (bandit) | `tox -e security` |
| Unit tests | `tox -e unit` |
| Integration tests | `tox -e integ` |
| Dependency audit (pip-audit) | `tox -e audit` |
| Re-lock all dependencies | `tox -e lock` |

Run `tox` before every commit.
Before each release, also run: `tox -e lock`, then `tox -e audit`, then `tox -e integ`.

To fix formatting issues reported by `tox -e lint`, run `ruff format .` locally then re-run tox.
To re-lock all requirements files after editing any `.in` counterpart: `tox -e lock`.

### Tool configuration

Prefer individual configuration files per tool (e.g., `.bandit`, `mypy.ini`, `ruff.toml`) over consolidating everything into `pyproject.toml`. Use `pyproject.toml` only for package metadata and build system configuration.

## Development workflow

Every change (feature, bug fix, refactoring, …) follows this process:

1. **Create a branch**: one branch per change, named after the intent (e.g., `feat/search-by-rank`).
2. **Write a plan**: create `PLAN.md` at the repo root on the branch; describe the steps before writing any code. One step = one future commit.
3. **Review the plan**: adapt it before starting execution.
4. **Execute step by step** — for each step in `PLAN.md`:
   - Edit code and adapt tests.
   - Review the changes.
   - Run `tox` (full quality gate).
   - Loop until clean.
   - Commit.
5. **Run integration tests**: `tox -e integ`; loop until clean.
6. **Release**: bump to next patch version (`Z` in `X.Y.Z`), update `CHANGELOG.md`, run `tox -e lock && tox -e audit`, tag `version/X.Y.Z`.

### Step quality rules

Each step (commit) must be:
- **Localized**: touch as few files as possible — ideally one; as few sections within that file as possible.
- **Consistent**: all changes in the step serve a single, coherent purpose.
- **Clean**: the codebase must pass `tox` at the end of every step, with no known errors left behind.

`PLAN.md` is branch-local and must **not** be merged into `main`.

## Architecture

### Modularization

Modules are organized in layers. Inner layers never import from outer layers:

```
cli.py → search.py → _protocol.py → models.py
                   ↘ exceptions.py
_client.py → _protocol.py, models.py, exceptions.py
```

Rules:

- `models.py` and `exceptions.py`: no imports from this package.
- `_protocol.py`: imports `models.py` only; defines `BggClientProtocol` (`typing.Protocol`).
- `_client.py`: internal (underscore prefix); never imported directly by callers; implements `BggClientProtocol`.
- `search.py`: depends on `BggClientProtocol`, not on `_client.py`; receives a client instance via parameter.
- `cli.py`: pure I/O adapter — parse args, call `search.py`, format output; no business logic.
- `__init__.py`: explicitly re-exports the public API; adding internal modules never accidentally becomes public.

### Code conventions

- **Python 3.13**; use built-in `tomllib`, `match`/`case`, `TypeAlias`, etc. where appropriate.
- Public functions and classes must have type annotations; internal helpers may omit them only when obvious.
- No comments that restate what the code already says. Comment the *why*, not the *what*.
- Raise domain-specific exceptions (subclass `BggSearchError`) instead of leaking `httpx` errors.

### Package selection rules

When choosing packages, apply these rules in order:

1. **Prefer stdlib** over external packages when the functionality is equivalent.
2. **Prefer well-maintained external packages**: large community, frequent and recent releases.
3. **Prefer packages with fewer transitive dependencies** when other criteria are equal.

Concretely for this project:
- XML parsing → `xml.etree.ElementTree` (stdlib), not `lxml` or `beautifulsoup4`
- HTTP → `httpx` (active community, minimal deps) over `requests` (heavier dep tree) or `aiohttp`
- Data models → `dataclasses` (stdlib) when validation is not needed; `pydantic>=2` only when input validation is required
- Date/time → `datetime` (stdlib), not `arrow` or `pendulum`

### Testing

Use `pytest`; never use `unittest` directly.
Aim for behavior coverage, not line coverage — test what the public API promises, not implementation details.

#### Unit tests (`tests/unit/`)

- Purely local: no network, no filesystem side-effects.
- Mock HTTP with `httpx.MockTransport`; do **not** add `pytest-httpx`.
- One file per source module: `tests/unit/test_client.py`, `tests/unit/test_search.py`, etc.
- Must run fast; run automatically after every code change.

#### Integration tests (`tests/integ/`)

- Hit the real BGG API; require network access.
- Run only explicitly (e.g., before a release) — never triggered automatically.
- Keep the number of requests minimal: one test must not make more API calls than strictly necessary.
- Add a `time.sleep` between requests to avoid flooding the BGG API.
- One file per high-level scenario: `tests/integ/test_search_flow.py`, etc.

### Things to avoid

- Do **not** add logging configuration at module level; leave that to the caller.
- Do **not** cache BGG responses unless caching is explicitly requested.
- Do **not** commit `.venv/`, `__pycache__/`, or `*.egg-info/` (ensure `.gitignore` covers them).

## Conventions

### Language

Use American English for text (messages, documentation, commits...)

### Commit format

Use commits of the form `<action>(<scope>):<description>`, where:

- `<action>` is one of "add", "upd", "feat", "refactor", "chore"...
- `<scope>` is a compact spec of the files full path (relative to project root)  
  (exceptionally it may be omitted, when the commit concerns the whole project)
- `<description>` is a short sentence describing the modification (do not repeat the action)

### Version management

Versions follow [Semantic Versioning](https://semver.org) (`MAJOR.MINOR.PATCH`):

- **MAJOR**: incompatible API change.
- **MINOR**: new backward-compatible feature.
- **PATCH**: backward-compatible bug fix.

Between releases the version carries the `.dev0` suffix (PEP 440), signalling that the code is not yet a stable build. The canonical workflow:

1. Before release: set version to `X.Y.Z` in `pyproject.toml`, update `CHANGELOG.md`, commit, tag `version/X.Y.Z`.
2. After release: immediately bump to `X.Y.(Z+1).dev0` (or the appropriate next segment) and commit.

The version is declared once, in `pyproject.toml` (`version = "..."`); the package exposes it via `importlib.metadata`:

```python
from importlib.metadata import version
__version__ = version("bgg-search")
```

Do **not** hard-code the version string anywhere else in the source.

### Changelog

`CHANGELOG.md` follows the [Keep a Changelog](https://keepachangelog.com) format (version 1.0.0).

Rules:

- Always keep an `## [Unreleased]` section at the top.
- Add an entry under `[Unreleased]` for every user-facing change (new feature, fix, removed behavior). Internal refactors and tooling changes do not need an entry.
- Use the standard subsections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- On release: rename `[Unreleased]` to `[x.y.z] - YYYY-MM-DD` and open a fresh `[Unreleased]` section above it.
- Do **not** edit past release sections.

## Reference

### BGG XML API2

Base URL: `https://boardgamegeek.com/xmlapi2/`

Key endpoints used in this project:

| Endpoint | Purpose |
|----------|---------|
| `search?query=<q>&type=boardgame` | Search games by name |
| `thing?id=<id>&stats=1` | Fetch full game details |
| `collection?username=<u>&own=1` | Fetch a user's owned games |

The API is unauthenticated and rate-limited; add a short `time.sleep` between bulk requests.
