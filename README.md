# bgg-search

`bgg-search` is a Python package and command-line tool for querying the
[BoardGameGeek](https://boardgamegeek.com) XML API. It lets you search for board games
by name and retrieve full game details — player counts, play time, weight, BGG rating, and
more — from the command line or from your own Python code.

**Contents:**

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [Development](#development)

## Installation

```bash
pip install bgg-search
```

Requires **Python ≥ 3.13**.

A BGG API token is required to make requests. Obtain one by registering your application at
<https://boardgamegeek.com/applications>.

The token is resolved in this order — the first source found is used:

1. **`--token-file PATH`** — CLI option pointing to a file containing the token.
2. **`BGG_TOKEN`** — environment variable.
3. **`.bgg-token`** — plain-text file in the current working directory.

If none of the above is provided, the command exits with code 1 and prints an error to stderr.

## Quickstart

### CLI

```bash
export BGG_TOKEN=<your-token>

# Search for games matching a query
bgg-search search "Catan"
#       13  Catan
#   396790  Catan: New Energies
#      ...

# Fetch full details for a game by its BGG ID
bgg-search details 13
# id:            13
# name:          Catan
# year:          1995
# min_players:   3
# max_players:   4
# ...
```

### Python API

```python
import os
from bgg_search import BggClient, search_games, get_game

client = BggClient(token=os.environ["BGG_TOKEN"])

results = search_games("Catan", client)
for game in results:
    print(game.id, game.name)

details = get_game(13, client)
print(details.name, details.bgg_rating)
```

## Documentation

- [Python API reference](https://arnauldvm.github.io/bgg-search/)
- [CLI reference](https://arnauldvm.github.io/bgg-search/cli.html)

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
