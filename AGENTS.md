# BGG Search — Agent Guide

## Project overview

`bgg-search` is a personal Python package for querying [BoardGameGeek](https://boardgamegeek.com) (BGG).
It wraps the BGG XML API2 and exposes a clean Python interface for searching games, retrieving game details,
and filtering results.

This is a personal project; prioritize clarity and correctness over enterprise-grade robustness.

Rationale behind key choices is documented in [DECISIONS.md](DECISIONS.md).

## Repository layout (target structure)

```
bgg-search/
├── src/
│   └── bgg_search/          # installable package
│       ├── __init__.py
│       ├── client.py        # HTTP client / API wrapper
│       ├── models.py        # dataclasses / Pydantic models
│       └── search.py        # high-level search helpers
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
├── README.md
└── AGENTS.md
```

## Language

Use American English for text (messages, documentation, commits...)

## Code versioning

Use commits of the form `<action>(<scope>):<description'>`, where:

- `<action>` is one of "add", "upd", "feat", "refactor", "chore"...
- `<scope>` is a compact spec of the files full path (relative to project root)  
  (exceptionally it may be omitted, when the commit concerns the whole project)
- `<description>` is a short sentence describing the modification (do not repeat the action)

## Development environment

Dependencies are managed with **uv**. Each context has its own requirements file (see `requirements/`).
`.in` files are the unpinned specs; `.txt` files are the locked versions generated from them.

```bash
# create and activate a virtual environment
uv venv && source .venv/bin/activate

# install the package in editable mode with locked dev deps
uv pip install -e . -r requirements/dev.txt
```

To re-lock all requirements files after editing any `.in` counterpart: `tox -e lock`.

There is no `setup.py`. `pyproject.toml` contains package metadata and build system only; all dependency declarations live in `requirements/`.

## Commands

Tests are automated with **tox**, which runs each step in an isolated virtualenv.

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

## Code conventions

- **Python 3.13**; use built-in `tomllib`, `match`/`case`, `TypeAlias`, etc. where appropriate.
- Prefer **dataclasses** or **Pydantic v2** models over raw dicts for API responses.
- HTTP calls go through `httpx` (sync client is fine; async only if explicitly needed).
- Parse XML with the standard library `xml.etree.ElementTree`; avoid third-party XML libs.
- Public functions and classes must have type annotations; internal helpers may omit them only when obvious.
- No comments that restate what the code already says. Comment the *why*, not the *what*.
- Raise domain-specific exceptions (subclass `BggSearchError`) instead of leaking `httpx` errors.

## Testing

Use `pytest`; never use `unittest` directly.
Aim for behavior coverage, not line coverage — test what the public API promises, not implementation details.

### Unit tests (`tests/unit/`)

- Purely local: no network, no filesystem side-effects.
- Mock HTTP with `httpx.MockTransport`; do **not** add `pytest-httpx`.
- One file per source module: `tests/unit/test_client.py`, `tests/unit/test_search.py`, etc.
- Must run fast; run automatically after every code change.

### Integration tests (`tests/integ/`)

- Hit the real BGG API; require network access.
- Run only explicitly (e.g., before a release) — never triggered automatically.
- Keep the number of requests minimal: one test must not make more API calls than strictly necessary.
- Add a `time.sleep` between requests to avoid flooding the BGG API.
- One file per high-level scenario: `tests/integ/test_search_flow.py`, etc.

## Package selection rules

When choosing packages, apply these rules in order:

1. **Prefer stdlib** over external packages when the functionality is equivalent.
2. **Prefer well-maintained external packages**: large community, frequent and recent releases.
3. **Prefer packages with fewer transitive dependencies** when other criteria are equal.

Concretely for this project:
- XML parsing → `xml.etree.ElementTree` (stdlib), not `lxml` or `beautifulsoup4`
- HTTP → `httpx` (active community, minimal deps) over `requests` (heavier dep tree) or `aiohttp`
- Data models → `dataclasses` (stdlib) when validation is not needed; `pydantic>=2` only when input validation is required
- Date/time → `datetime` (stdlib), not `arrow` or `pendulum`

## Tool configuration

Prefer individual configuration files per tool (e.g., `.bandit`, `mypy.ini`, `ruff.toml`) over consolidating everything into `pyproject.toml`. Use `pyproject.toml` only for package metadata and build system configuration.

## Things to avoid

- Do **not** add `setup.cfg` or `setup.py`.
- Do **not** use `requests`; the project uses `httpx`.
- Do **not** add logging configuration at module level; leave that to the caller.
- Do **not** cache BGG responses unless caching is explicitly requested.
- Do **not** commit `.venv/`, `__pycache__/`, or `*.egg-info/` (ensure `.gitignore` covers them).

## BGG XML API2 reference

Base URL: `https://boardgamegeek.com/xmlapi2/`

Key endpoints used in this project:

| Endpoint | Purpose |
|----------|---------|
| `search?query=<q>&type=boardgame` | Search games by name |
| `thing?id=<id>&stats=1` | Fetch full game details |
| `collection?username=<u>&own=1` | Fetch a user's owned games |

The API is unauthenticated and rate-limited; add a short `time.sleep` between bulk requests.
