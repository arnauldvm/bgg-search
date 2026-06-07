# Step 7 — Update `AGENTS.md`

## Step 1 — Repository layout: add `scripts/`

`AGENTS.md`: add `scripts/` directory entry with `release.py` to the repository layout tree.

## Step 2 — Commands table: add `tox -e release`

`AGENTS.md`: add `tox -e release` row to the commands table.

## Step 3 — Release procedure: automate with single command

`AGENTS.md`: replace the manual step list with `BGG_TOKEN=<token> tox -e release` as the
invocation; move the 11 steps under a `### Steps performed by the script` subsection so
the detail is kept as a reference.
