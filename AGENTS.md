# BGG Search — Agent Guide

## Project overview

`bgg-search` is a personal Python package for querying [BoardGameGeek](https://boardgamegeek.com) (BGG).
It wraps the BGG XML API2 and exposes a clean Python interface for searching games, retrieving game details,
and filtering results.

This is a personal project; prioritize clarity and correctness over enterprise-grade robustness.

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
│   └── test_*.py
├── pyproject.toml           # build system, deps, tool config
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

```bash
# create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# install the package in editable mode with dev dependencies
pip install -e ".[dev]"
```

All tooling is configured in `pyproject.toml`. There is no `setup.py` or `requirements.txt`.

## Commands

| Task | Command |
|------|---------|
| Run tests | `pytest` |
| Type-check | `mypy src/` |
| Lint / format | `ruff check . && ruff format .` |

Run all three before committing:

```bash
ruff check . && ruff format . && mypy src/ && pytest
```

## Code conventions

- **Python ≥ 3.11**; use built-in `tomllib`, `match`/`case`, `TypeAlias`, etc. where appropriate.
- Prefer **dataclasses** or **Pydantic v2** models over raw dicts for API responses.
- HTTP calls go through `httpx` (sync client is fine; async only if explicitly needed).
- Parse XML with the standard library `xml.etree.ElementTree`; avoid third-party XML libs.
- Public functions and classes must have type annotations; internal helpers may omit them only when obvious.
- No comments that restate what the code already says. Comment the *why*, not the *what*.
- Raise domain-specific exceptions (subclass `BggSearchError`) instead of leaking `httpx` errors.

## Testing

- Use `pytest` with `pytest-httpx` to mock HTTP responses; never hit the real BGG API in tests.
- Fixtures live in `tests/conftest.py`.
- One file per module under test: `tests/test_client.py`, `tests/test_search.py`, etc.
- Aim for behavior coverage, not line coverage — test what the public API promises, not implementation details.

## Dependencies (expected `pyproject.toml` extras)

```toml
[project]
dependencies = ["httpx", "pydantic>=2"]

[project.optional-dependencies]
dev = ["pytest", "pytest-httpx", "mypy", "ruff"]
```

## Things to avoid

- Do **not** add `setup.cfg`, `setup.py`, or a `requirements.txt`.
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
