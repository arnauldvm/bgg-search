# Plan — doc/complete-readme

Implements PHASE_PLAN Step 4 only. Each sub-step is one commit.
All changes are within `README.md`.

## Sub-step 1 — Introduction + Installation

Replace the stub notice with a one-paragraph introduction and an Installation section
(pip install command, Python ≥ 3.13 requirement, BGG token note).

Commit: `upd(README.md): add introduction and installation sections`

---

## Sub-step 2 — Quickstart

Add a Quickstart section with two short examples: CLI usage and Python API (3–5 lines each).

Commit: `upd(README.md): add quickstart section`

---

## Sub-step 3 — Python API reference

Add a Python API reference section covering `search_games`, `get_game`,
`BggClientProtocol`, all model fields (`GameSummary`, `GameDetails`),
and all exception classes.

Commit: `upd(README.md): add Python API reference section`

---

## Sub-step 4 — CLI reference

Add a CLI reference section documenting `bgg-search search` and `bgg-search details`
with arguments and output format.

Commit: `upd(README.md): add CLI reference section`
