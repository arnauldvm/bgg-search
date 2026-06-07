# Plan — feat/search-use-case-layer

Implements PHASE_PLAN Step 1 only. Each sub-step is one commit.

## Sub-step 1 — `search_games` in `search.py` + its tests

**`src/bgg_search/search.py`** (new file)

- `search_games(query: str, client: BggClientProtocol) -> list[GameSummary]`
  — delegates to `client.search(query)`.

**`tests/unit/test_search.py`** (new file)

- `test_search_games_delegates_to_client` — mock client, verify delegation and return value.
- `test_search_games_returns_empty_list` — mock returns `[]`, verify propagated.

Commit: `feat(src/bgg_search/search.py): add search_games use-case function`

---

## Sub-step 2 — `get_game` in `search.py` + its tests

**`src/bgg_search/search.py`**

- `get_game(game_id: int, client: BggClientProtocol) -> GameDetails`
  — delegates to `client.get_game(game_id)`.

**`tests/unit/test_search.py`**

- `test_get_game_delegates_to_client` — mock client, verify delegation and return value.
- `test_get_game_propagates_not_found` — mock raises `BggNotFoundError`, verify re-raised.

Commit: `feat(src/bgg_search/search.py): add get_game use-case function`

---

## Sub-step 3 — `src/bgg_search/__init__.py`

Add `search_games` and `get_game` to imports and `__all__`.

Commit: `upd(src/bgg_search/__init__.py): expose search_games and get_game in public API`

---

## Sub-step 4 — `CHANGELOG.md`

Add under `[Unreleased]`:

```markdown
### Added
- `search_games(query, client)` and `get_game(game_id, client)` use-case functions.
```

Commit: `upd(CHANGELOG.md): document search_games and get_game under [Unreleased]`
