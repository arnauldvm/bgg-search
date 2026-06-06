# Phase 0.2 — Domain & protocol: plan

**Goal**: establish the stable core that all other layers depend on — no HTTP, no I/O.

Each modification below is one short-lived feature branch merged into `main`.
Each branch follows the standard development workflow (PLAN.md → tox → merge --no-ff).

---

## Summary table

| # | Branch | Files touched | Summary |
|---|--------|---------------|---------|
| 1 | `feat/models` | `models.py` *(new)*, `tests/unit/test_models.py` *(new)* | Pure domain dataclasses + unit tests |
| 2 | `feat/exceptions` | `exceptions.py` *(new)*, `tests/unit/test_exceptions.py` *(new)* | Domain exception hierarchy + unit tests |
| 3 | `feat/protocol` | `_protocol.py` *(new)* | `BggClientProtocol` structural interface |
| 4 | `feat/public-api` | `__init__.py` *(update)*, `CHANGELOG.md` *(update)* | Explicit public API surface + changelog |

Modifications 1 and 2 are independent and may be executed in either order (or as concurrent
branches), but both must be merged before modification 3 begins.

---

## Modification 1 — `feat/models`

**Branch**: `feat/models`

**Files touched**:
- `src/bgg_search/models.py` *(new)*
- `tests/unit/test_models.py` *(new)*

**Goal**: define the pure domain dataclasses that represent BGG data.

**Models** (all `@dataclass(frozen=True)`):

| Class | Fields |
|-------|--------|
| `GameSummary` | `id: int`, `name: str` |
| `GameDetails` | `id: int`, `name: str`, `year_published: int \| None`, `min_players: int \| None`, `max_players: int \| None`, `min_playtime: int \| None`, `max_playtime: int \| None`, `weight: float \| None`, `bgg_rating: float \| None` |

`GameSummary` is what the `search` endpoint returns; `GameDetails` is what the `thing`
endpoint returns.

No imports from this package. No validation — raw values from the API are trusted here.

**Tests**: construction with all fields, immutability (frozen), field access. No HTTP.

---

## Modification 2 — `feat/exceptions`

**Branch**: `feat/exceptions`

**Files touched**:
- `src/bgg_search/exceptions.py` *(new)*
- `tests/unit/test_exceptions.py` *(new)*

**Goal**: define the domain exception hierarchy so that callers never see raw `httpx` or
`xml.etree` errors.

**Hierarchy**:

```
BggSearchError          # base; all public exceptions are subclasses of this
  BggApiError           # HTTP-level failure (non-200, timeout, …); carries status_code: int | None
  BggNotFoundError      # requested game ID not found in the API response
  BggParseError         # API returned unexpected XML structure
```

No imports from this package.

**Tests**: construction with all arguments, `isinstance` hierarchy checks, and message
propagation. Verify that every concrete exception is a `BggSearchError`.

---

## Modification 3 — `feat/protocol`

**Branch**: `feat/protocol`  
**Depends on**: modifications 1 and 2 merged into `main`

**Files touched**:
- `src/bgg_search/_protocol.py` *(new)*

**Goal**: define `BggClientProtocol` — the structural interface between the use-case layer
(`search.py`, phase 0.4) and the HTTP layer (`_client.py`, phase 0.3).

**Protocol** (`typing.Protocol`, `@runtime_checkable`):

```python
class BggClientProtocol(Protocol):
    def search(self, query: str) -> list[GameSummary]: ...
    def get_game(self, game_id: int) -> GameDetails: ...
```

Imports from `models.py` only. Exceptions are raised by implementors, not declared in the
protocol.

No unit tests for this modification: a `Protocol` carries no runtime behavior to test.

---

## Modification 4 — `feat/public-api`

**Branch**: `feat/public-api`  
**Depends on**: modifications 1, 2, and 3 merged into `main`

**Files touched**:
- `src/bgg_search/__init__.py` *(update)*
- `CHANGELOG.md` *(update)*

**Goal**: make the public API surface explicit. Callers do `import bgg_search` and access
exactly the symbols listed below — nothing more leaks through.

**Re-exports** and `__all__`:

```python
from bgg_search.models import GameSummary, GameDetails
from bgg_search.exceptions import BggSearchError, BggApiError, BggNotFoundError, BggParseError
from bgg_search._protocol import BggClientProtocol

__all__ = [
    "__version__",
    "GameSummary",
    "GameDetails",
    "BggSearchError",
    "BggApiError",
    "BggNotFoundError",
    "BggParseError",
    "BggClientProtocol",
]
```

**CHANGELOG entry** (under `## [Unreleased]`, subsection `Added`):
> Public API surface: `GameSummary`, `GameDetails`, `BggSearchError`, `BggApiError`,
> `BggNotFoundError`, `BggParseError`, `BggClientProtocol`.

No new tests needed (re-exports are structural; coverage is already provided by the tests
in modifications 1 and 2).

---

## Release checklist (after all modifications merged)

- [ ] `tox` passes clean on `main`
- [ ] `tox -e lock` — regenerate locked deps if any were added
- [ ] `tox -e audit` — dependency audit clean
- [ ] `tox -e integ` — integration tests pass (none exist in this phase; trivially clean)
- [ ] Bump version to `0.2.0`, update `CHANGELOG.md`, commit, tag `version/0.2.0`
- [ ] Bump to `0.3.0.dev0`, commit
- [ ] Push `main`, then push `version/0.2.0`
