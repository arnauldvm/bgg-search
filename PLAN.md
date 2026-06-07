# Step 3 — Markdown linting in `tox -e lint`

## Step 1 — Add `pymarkdownlnt` to dev dependencies
`requirements/dev.in`: add `pymarkdownlnt~=0.9.37`.
`requirements/dev.txt`: regenerate with `tox -e lock`.

## Step 2 — Configure `pymarkdownlnt`
`.pymarkdown.json`: enforce ATX-only headings (MD003).

## Step 3 — Add `pymarkdown scan` to `tox -e lint`
`tox.ini`: add `pymarkdown scan` command to `[testenv:lint]`.
