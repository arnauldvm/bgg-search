# Project process

## Project initiation workflow

Used once, from project creation to MVP (`1.0.0`):

1. **Prepare `AGENTS.md`** — customize for the project before writing any code.
2. **High-level plan** — propose a succession of broad phases, each delivering a coherent layer or capability. Versions: `0.1.x`, `0.2.x`, … Store in `HIGHLEVEL_PLAN.md`.
3. **Review** — adapt the high-level plan before proceeding.
4. **Execute phases** — for each phase:
   - 4.1 Propose a detailed phase plan (decomposed into successive modifications). Store in `PHASE_PLAN.md` on the phase branch.
   - 4.2 Review and adapt the phase plan.
   - 4.3 Implement each modification following the **Development workflow** (see [AGENTS.md](AGENTS.md)).
   - 4.4 Release the phase (`0.N.0`).
5. **Release MVP** — tag `version/1.0.0`.

After MVP, switch to a pure incremental workflow: one small feature at a time, each following the **Development workflow**.
