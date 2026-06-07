# Plan — upd/integ-test-use-case-layer

Implements PHASE_PLAN Step 3 only. Each sub-step is one commit.
All changes are within `tests/integ/test_search_flow.py`.

## Sub-step 1 — Imports + fixture

Replace the `BggClient`-only import with `BggClientProtocol`-agnostic imports.
Rename the `bgg_client` fixture to `client` and update its return type annotation to
`BggClientProtocol`, to reflect that callers no longer depend on the concrete type.

Commit: `upd(tests/integ/test_search_flow.py): rename fixture, use BggClientProtocol type`

---

## Sub-step 2 — `test_search_returns_results`

Replace `bgg_client.search("Catan")` with `search_games("Catan", client)`.

Commit: `upd(tests/integ/test_search_flow.py > test_search_returns_results): use use-case layer`

---

## Sub-step 3 — `test_get_game_returns_details`

Replace `bgg_client.get_game(_CATAN_ID)` with `get_game(_CATAN_ID, client)`.

Commit: `upd(tests/integ/test_search_flow.py > test_get_game_returns_details): use use-case layer`
