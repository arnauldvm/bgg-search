# Project process

## Project initiation workflow

Used once, from project creation to MVP (`1.0.0`):

1. **Prepare `AGENTS.md`** — customize for the project before writing any code.
2. **Roadmap** — propose a succession of broad phases, each delivering a coherent layer or capability. Versions: `0.1.x`, `0.2.x`, … Store in `ROADMAP.md`.
3. **Review** — adapt the roadmap before proceeding.
4. **Execute phases** — for each phase:
   - 4.1 Propose a detailed phase plan (decomposed into successive modifications). Commit `PHASE_PLAN.md` to `main`.
   - 4.2 Review and adapt the phase plan.
   - 4.3 Implement each modification following the **Development workflow** (see [AGENTS.md](AGENTS.md)).
   - 4.4 Remove `PHASE_PLAN.md` in a dedicated commit on `main` before releasing.
   - 4.5 Release the phase (`0.N.0`).
5. **Release MVP** — tag `version/1.0.0`.

After MVP, switch to a pure incremental workflow: one small feature at a time, each following the **Development workflow**.

## Branch and version map

```
main
 │
 ○ 0.1.0.dev0
 │   ┌── feat/A ──┐
 │   └────────────○ merge
 │   ┌── feat/B ──┐
 │   └────────────○ merge
 ○ 0.1.0 ◄── Phase 1 release
 │
 ○ 0.2.0.dev0
 │   ┌── feat/C ──┐
 │   └────────────○ merge
 ○ 0.2.0 ◄── Phase 2 release
 │   ...
 ○ 1.0.0 ◄── MVP
 │
 │  (incremental)
 │   ┌── feat/D ──┐
 │   └────────────○ merge + tag 1.1.0   ← new feature → bump Y
 │   ┌── fix/E ───┐
 │   └────────────○ merge + tag 1.2.0   ← significant fix → bump Y
 │
 | (hotfix on a past version — branch from old tag, not from main)
 |\
 | ┌── hotfix/F ──┐
 | └──────────────○ tag 1.0.1           ← hotfix → bump Z
...
```

**Key rules:**
- All feature branches are short-lived, cut from `main`, merged back to `main`.
- During initiation phases: feature merges do not produce individual releases; only the phase boundary does (`0.N.0`).
- Post-MVP: each change is released immediately after merge.
  - New feature or significant fix on the latest version → bump **Y**.
  - Hotfix backported to a past version → bump **Z** (branch cut from the old release tag, not `main`).
- `PLAN.md` is branch-local and never merged to `main`.
- `PHASE_PLAN.md` lives on `main` during the phase and is removed before the phase release.
