# bgg-search

`bgg-search` is a Python package and command-line tool for querying the
[BoardGameGeek](https://boardgamegeek.com) XML API. It lets you search for board games
by name and retrieve full game details — player counts, play time, weight, BGG rating, and
more — from the command line or from your own Python code.

## Installation

```bash
pip install bgg-search
```

Requires **Python ≥ 3.13**.

A BGG API token is required to make requests. Obtain one by registering your application at
<https://boardgamegeek.com/applications>, then expose it as the `BGG_TOKEN` environment
variable.

## Development

Run the quality gate (lint, type-check, security scan, unit tests):

```bash
tox
```

Run integration tests against the real BGG API:

```bash
BGG_TOKEN=<your-token> tox -e integ
```

A BGG API token is required. Obtain one by registering your application at
<https://boardgamegeek.com/applications>. Tests are skipped automatically when
`BGG_TOKEN` is not set.
