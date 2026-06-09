# Plan — fix MVP version references

Replace every assertion that `1.0.0` is the MVP with the correct fact that `0.5.0` is the MVP.
The classifier (`3 - Alpha`) is already correct and needs no change.

## Steps

1. **ROADMAP.md** — fix intro line, version table, and post-MVP section:
   - Intro: "Phases toward `1.0.0` (MVP)" →
     "Phases toward the MVP release (`0.5.0`), reached, and beyond"
   - Version table: remove the `1.0.0` row; mark `0.5.0` as MVP in its row
   - Post-MVP section text: "After `1.0.0`, development switches…" →
     "After `0.5.0` (MVP), development switches…"

2. **PROCESS.md** — fix initiation workflow and branch diagram:
   - Step description: "from project creation to MVP (`1.0.0`)" → "from project creation to MVP (`0.5.0`)"
   - Step 5: "tag `version/1.0.0`" → "the last phase release IS the MVP (reached at `0.5.0`)"
   - Diagram: `○ 1.0.0 ◄── MVP` → `○ 0.5.0 ◄── MVP`

3. **AGENTS.md** — fix file-table description:
   - "succession of phases toward MVP" → "succession of phases toward MVP (reached at `0.5.0`)"
