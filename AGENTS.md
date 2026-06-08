# BGG Search — Agent Guide

**Contents:**

- [Project context](#project-context)
- [Development environment](#development-environment)
- [Development workflow](#development-workflow)
- [Release procedure](#release-procedure)
- [Architecture](#architecture)
- [Conventions](#conventions)
- [Reference](#reference)

## Project context

`bgg-search` is a personal Python package for querying
[BoardGameGeek](https://boardgamegeek.com) (BGG).
It wraps the BGG XML API2 and exposes:

- a clean, reusable Python API for searching games, retrieving game details, and filtering results;
- a generic CLI for interacting with the BGG API from the command line.

This is a personal project; prioritize clarity and correctness over enterprise-grade robustness.

Rationale behind key choices is documented in [DECISIONS.md](DECISIONS.md).
The project initiation workflow and branch/version map are documented in [PROCESS.md](PROCESS.md).

### Repository layout (target structure)

```text
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
├── scripts/
│   └── release.py           # automated release script (invoked via tox -e release)
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
├── CHANGELOG.md             # user-facing change history (Keep a Changelog format)
├── DECISIONS.md             # rationale behind key design and package choices
├── PROCESS.md               # project initiation workflow and branch/version map
├── README.md                # public-facing project documentation
└── AGENTS.md                # guide for AI agents (this file)
```

Transient files (not always present):

| File | Scope | Purpose |
|------|-------|---------|
| `ROADMAP.md` | `main` | succession of phases toward MVP |
| `PHASE_PLAN.md` | `main` | decomposition of the current phase |
| `PLAN.md` | feature branch | steps for the current feature/change |

## Development environment

Dependencies are managed with **uv**.
Each context has its own requirements file (see `requirements/`).
`.in` files are the unpinned specs; `.txt` files are the locked versions generated from them.

```bash
# create and activate a virtual environment
uv venv --python 3.13 && source .venv/bin/activate

# install the package in editable mode with locked dev deps
uv pip install -e . -r requirements/dev.txt

# register the pre-commit hook (once per clone)
pre-commit install
```

There is no `setup.py`. `pyproject.toml` contains package metadata and build system only;
all dependency declarations live in `requirements/`.

### Commands

All tasks run through **tox**, which executes each step in an isolated virtualenv.

| Task | Command |
|------|---------|
| Full quality gate (lint + type + security + unit tests) | `tox` |
| Lint / format | `tox -e lint` |
| Type-check | `tox -e type` |
| Security scan (bandit) | `tox -e security` |
| Unit tests | `tox -e unit` |
| Integration tests | `BGG_TOKEN=<token> tox -e integ` |
| Dependency audit (pip-audit) | `tox -e audit` |
| Re-lock all dependencies | `tox -e lock` |
| Release | `BGG_TOKEN=<token> tox -e release` |
| Release (local only, no PyPI publish) | `BGG_TOKEN=<token> tox -e release-no-publish` |

The pre-commit hook runs `tox` automatically before every commit and blocks if any check fails.

To fix formatting issues reported by `tox -e lint`, run `ruff format .` locally then re-run tox.

### Tool configuration

Prefer individual configuration files per tool (e.g., `.bandit`, `mypy.ini`, `ruff.toml`)
over consolidating everything into `pyproject.toml`.
Use `pyproject.toml` only for package metadata and build system configuration.

## Development workflow

Every change (feature, bug fix, refactoring, …) follows this process:

1. **Create a branch**: cut a short-lived branch from `main`, named after the intent
   (e.g., `feat/search-by-rank`).
2. **Write a plan**: create `PLAN.md` on the branch; describe the steps before writing any code.
   One step = one future commit.
   Commit `PLAN.md` immediately so it is tracked and stays branch-local.
   (`PLAN.md` is the feature-level plan; the phase-level plan lives in `PHASE_PLAN.md` on `main`
   — see [PROCESS.md](PROCESS.md).)
3. **Review the plan**: adapt it before starting execution.
4. **Execute step by step** — for each step in `PLAN.md`:
   - Edit code and adapt tests.
   - If the change is user-facing, add an entry to `CHANGELOG.md` under `## [Unreleased]`.
   - Review the changes.
   - Commit — the pre-commit hook runs `tox` automatically and blocks if any check fails;
     fix issues and retry.
5. **Remove `PLAN.md`**: delete it in a dedicated commit
   (`chore(PLAN.md): remove branch-local plan before merge`).
   This ensures it is never merged into `main`.
6. **Merge and delete the branch**: merge into `main` with `--no-ff`, then delete the branch
   (`git branch -d <branch>`).
   Push `main` to remote immediately after every merge: `git push origin main`.
7. **Push regularly**: any direct commits on `main` (e.g. `PHASE_PLAN.md` updates) must also
   be pushed promptly. Do not let `main` drift ahead of `origin/main` for more than one commit.
8. **Remove `PHASE_PLAN.md`**: delete it in a dedicated commit on `main` before releasing.
   This ensures the plan is gone before the release tag is created.
9. **Release**: follow the [Release procedure](#release-procedure) section below.

### Step quality rules

Each step (commit) must be:

- **Localized**: touch as few files as possible — ideally one;
  as few sections within that file as possible.
- **Consistent**: all changes in the step serve a single, coherent purpose.
- **Clean**: the codebase must pass `tox` at the end of every step
  (enforced by the pre-commit hook), with no known errors left behind.

`PLAN.md` is branch-local and must **not** be merged into `main` (enforced by step 5 above).

### Plan file conventions

All plan files (`ROADMAP.md`, `PHASE_PLAN.md`, `PLAN.md`) track completion inline.
Mark each deliverable or step done by prepending `✓` (followed by a space) to its bullet as
soon as the work is committed. The mark must be part of the same commit as the work it tracks
— do not defer or batch-update plan files at the end of a step or phase.

## Release procedure

```bash
BGG_TOKEN=<token> tox -e release
```

The script verifies all preconditions, runs the full quality gate, bumps versions,
commits, tags, pushes, and polls PyPI — aborting with a clear message on any failure.
Pass `--help` for available options
(`--check-only`, `--no-publish`, `--verify-pypi`, `--verbose`, `bump`).

### Preconditions verified by the script

1. Current branch is `main`.
2. Working tree is clean (no staged or unstaged changes).
3. Current version in `pyproject.toml` ends in `.devN` (signals an unreleased development state).
4. The release tag `version/X.Y.Z` does not already exist locally or on the remote.
5. `BGG_TOKEN` environment variable is set (without it, integration tests silently skip
   and report success).
6. `CHANGELOG.md` has content under `[Unreleased]`
   (releasing with an empty section is almost certainly a mistake).
7. Local `main` is in sync with `origin/main` (not behind, not unexpectedly ahead).
8. `PHASE_PLAN.md` does not exist (see development workflow step 7).

### Steps performed by the script

1. Re-lock dependencies: `tox -e lock`
2. Audit dependencies: `tox -e audit`
3. Run integration tests: `tox -e integ`
4. Bump version in `pyproject.toml` to `X.Y.Z`.
5. Update `CHANGELOG.md`: rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` and open a
   fresh `[Unreleased]` section above it.
6. Commit: `chore: release X.Y.Z`
7. Tag: `git tag version/X.Y.Z`
8. Bump `pyproject.toml` to `X.(Y+1).0.dev0` and commit:
   `chore(pyproject.toml): bump version to X.(Y+1).0.dev0`
9. Push `main` first (the next-dev commit must be on the remote before the tag push triggers
   the publish workflow): `git push origin main`
10. Push the tag (triggers the publish workflow): `git push origin version/X.Y.Z`
11. Poll PyPI until the new version appears (retries every 30 s, up to 3 min).

## Architecture

### Modularization

Modules are organized in layers. Inner layers never import from outer layers:

```text
cli.py → search.py → _protocol.py → models.py
                   ↘ exceptions.py
_client.py → _protocol.py, models.py, exceptions.py
```

Rules:

- `models.py` and `exceptions.py`: no imports from this package.
- `_protocol.py`: imports `models.py` only; defines `BggClientProtocol` (`typing.Protocol`).
- `_client.py`: internal (underscore prefix); never imported directly by callers;
  implements `BggClientProtocol`.
- `search.py`: depends on `BggClientProtocol`, not on `_client.py`;
  receives a client instance via parameter.
- `cli.py`: pure I/O adapter — parse args, call `search.py`, format output; no business logic.
- `__init__.py`: explicitly re-exports the public API;
  adding internal modules never accidentally becomes public.

### Code conventions

- **Python 3.13**; use built-in `tomllib`, `match`/`case`, `TypeAlias`, etc. where appropriate.
- Public functions and classes must have type annotations;
  internal helpers may omit them only when obvious.
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
- Data models → `dataclasses` (stdlib) when validation is not needed;
  `pydantic>=2` only when input validation is required
- Date/time → `datetime` (stdlib), not `arrow` or `pendulum`

### Testing

Use `pytest`; never use `unittest` directly.
Aim for behavior coverage, not line coverage — test what the public API promises,
not implementation details.

#### Unit tests (`tests/unit/`)

- Purely local: no network, no filesystem side-effects.
- Mock HTTP with `httpx.MockTransport`; do **not** add `pytest-httpx`.
- One file per source module: `tests/unit/test_client.py`, `tests/unit/test_search.py`, etc.
- Must be fast enough to run after every code change.

#### Integration tests (`tests/integ/`)

- Hit the real BGG API; require network access.
- Require a BGG API token passed via the `BGG_TOKEN` environment variable;
  tests are skipped when it is absent.
- Run only explicitly (e.g., before a release) — never triggered automatically.
- Keep the number of requests minimal:
  one test must not make more API calls than strictly necessary.
- Add a `time.sleep` between requests to avoid flooding the BGG API.
- One file per high-level scenario: `tests/integ/test_search_flow.py`, etc.

### Things to avoid

- Do **not** add logging configuration at module level; leave that to the caller.
- Do **not** cache BGG responses unless caching is explicitly requested.
- Do **not** commit `.venv/`, `__pycache__/`, or `*.egg-info/` (ensure `.gitignore` covers them).

## Conventions

### Markdown

All Markdown files written or edited by agents must pass `markdownlint` without errors.
Common rules to observe:

- Line length must not exceed 100 characters.
- Fenced code blocks must declare a language (e.g. ` ```python `, ` ```toml `, ` ```markdown `).
- Headings must be surrounded by blank lines.
- No trailing spaces (except intentional line breaks).
- Lists must be preceded by a blank line.

The pre-commit hook enforces this automatically and will block commits that violate these rules.

### Spell checking

All files are spell-checked with `cspell` (config: `.cspell.yaml`).
When introducing a new technical term, proper noun, or domain-specific identifier that cspell
does not recognize, add it to the `words` list in `.cspell.yaml` in the same commit.
Include a short inline comment explaining what the word is.

Run `npx cspell "**" --no-progress` locally to verify before committing.

### Language

Use American English for text (messages, documentation, commits...)

### Commit format

Use commits of the form `<action>(<scope>):<description>`, where:

- `<action>` is one of "add", "upd", "feat", "refactor", "chore"...
- `<scope>` is a compact spec of the files full path (relative to project root)  
  (exceptionally it may be omitted, when the commit concerns the whole project);  
  optionally followed by `> <location>` to pinpoint the change within the file  
  (e.g. a class name, function name, or config section):
  `src/bgg_search/client.py > BggClient.search`
- `<description>` is a short sentence describing the modification (do not repeat the action)

Do not add `Co-Authored-By` trailers. AI involvement is documented once in this file.

### Version management

Versions follow [Semantic Versioning](https://semver.org) (`MAJOR.MINOR.PATCH`):

- **MAJOR**: incompatible API change.
- **MINOR**: new feature, or a significant fix on the latest version.
- **PATCH**: hotfix backported to a past version (branch cut from an old release tag, not `main`).

Between releases the version carries the `.dev0` suffix (PEP 440),
signalling that the code is not yet a stable build. The canonical workflow:

1. Before release: set version to `X.Y.Z` in `pyproject.toml`, update `CHANGELOG.md`, commit,
   tag `version/X.Y.Z`.
2. After release: immediately bump to `X.(Y+1).0.dev0` and commit.

The version is declared once, in `pyproject.toml` (`version = "..."`);
the package exposes it via `importlib.metadata`:

```python
from importlib.metadata import version
__version__ = version("bgg-search")
```

Do **not** hard-code the version string anywhere else in the source.

### Changelog

`CHANGELOG.md` follows the [Keep a Changelog](https://keepachangelog.com) format (version 1.0.0).

Rules:

- Always keep an `## [Unreleased]` section at the top.
- Add an entry under `[Unreleased]` for every user-facing change
  (new feature, fix, removed behavior). Internal refactors and tooling changes do not need an entry.
  The entry must be part of the same commit as the change — not deferred to release time.
- Use the standard subsections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- On release: rename `[Unreleased]` to `[x.y.z] - YYYY-MM-DD`
  and open a fresh `[Unreleased]` section above it.
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
