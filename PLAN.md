# Step 3 — Markdown linting via pre-commit

## Step 1 — Add `markdownlint-cli` to pre-commit

`.pre-commit-config.yaml`: add `markdownlint-cli` v0.48.0 hook.
`.markdownlint.yaml`: configure MD003 (atx), MD013 (line_length=100).

## Step 2 — Fix MD violations in existing Markdown files

`AGENTS.md`, `CHANGELOG.md`, `DECISIONS.md`, `PHASE_PLAN.md`, `PLAN.md`, `PROCESS.md`,
`ROADMAP.md`, `README.md`: fix violations so `pre-commit run markdownlint --all-files` passes.
