# Phase 0.3 — HTTP Client: Phase Plan

**Goal**: a working HTTP client that speaks to the BGG XML API, independently testable.

Deliverables:
- `src/bgg_search/_client.py` — concrete `httpx`-based implementation of `BggClientProtocol`.
- `tests/unit/test_client.py` — unit tests via `httpx.MockTransport` (no network).

---

## Step 1 — Add `httpx` runtime dependency

Feature branch: `feat/httpx-dep`

Files modified:
- `pyproject.toml` — add `httpx` to `dependencies`
- `requirements/runtime.in` — add `httpx~=0.28.0`
- `requirements/runtime.txt` — regenerate with `tox -e lock`

Notes:
- No source changes; this step wires the dependency only.
- `httpx.MockTransport` ships inside `httpx` itself, so no additional entry in `unit.in` is needed —
  the package is installed editable in the `unit` tox env and pulls its own runtime deps.

---

## Step 2 — `BggClient.search` + unit tests

Feature branch: `feat/bgg-client-search`

Files modified:
- `src/bgg_search/_client.py` — new file
- `tests/unit/test_client.py` — new file

### `BggClient` constructor + `search`

```
class BggClient:
    def __init__(self, *, base_url: str = "https://boardgamegeek.com/xmlapi2/", timeout: float = 10.0) -> None
    def search(self, query: str) -> list[GameSummary]
```

`search` hits `search?query=<query>&type=boardgame`, parses `<items>/<item>` elements via
`xml.etree.ElementTree`, and returns a `list[GameSummary]`.

### Error behavior

| Condition | Exception raised |
|-----------|-----------------|
| Non-2xx HTTP response | `BggApiError(message, status_code=<code>)` |
| XML that cannot be parsed by ElementTree | `BggParseError` |
| Required field absent or unparsable | `BggParseError` |

### Unit test outline

- `test_search_returns_summaries` — two `<item>` elements → two `GameSummary` objects
- `test_search_returns_empty_list` — `total="0"`, no `<item>` children → `[]`
- `test_search_raises_api_error_on_http_error` — mock returns HTTP 503 → `BggApiError(status_code=503)`
- `test_search_raises_parse_error_on_malformed_xml` — mock returns `<not valid` → `BggParseError`

---

## Step 3 — `BggClient.get_game` + unit tests + CHANGELOG

Feature branch: `feat/bgg-client-get-game`

Files modified:
- `src/bgg_search/_client.py` — add `get_game` method
- `tests/unit/test_client.py` — add `get_game` tests
- `CHANGELOG.md` — `Added` entry under `[Unreleased]`

### `get_game`

```
    def get_game(self, game_id: int) -> GameDetails
```

Hits `thing?id=<game_id>&stats=1`, parses the single `<item>` element. All `value` attributes
are parsed as integers or floats; missing optional attributes become `None` in `GameDetails`.

`BggClient` now fully implements `BggClientProtocol` (structural sub-typing; no explicit
`isinstance` check needed).

### Additional error behavior

| Condition | Exception raised |
|-----------|-----------------|
| Zero `<item>` elements in response | `BggNotFoundError` |

(HTTP and parse errors follow the same rules as `search`.)

### Unit test outline

- `test_get_game_returns_full_details` — all optional fields present → fully populated `GameDetails`
- `test_get_game_handles_missing_optional_fields` — optional fields absent → `None` values
- `test_get_game_raises_not_found` — zero `<item>` elements → `BggNotFoundError`
- `test_get_game_raises_api_error_on_http_error` — mock returns HTTP 503 → `BggApiError(status_code=503)`
- `test_get_game_raises_parse_error_on_malformed_xml` — mock returns `<not valid` → `BggParseError`
