# bgg-search

`bgg-search` is a Python package and command-line tool for querying the
[BoardGameGeek](https://boardgamegeek.com) XML API. It lets you search for board games
by name and retrieve full game details — player counts, play time, weight, BGG rating, and
more — from the command line or from your own Python code.

**Contents:**

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Python API reference](#python-api-reference)
- [CLI reference](#cli-reference)
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

## Python API reference

### Use-case functions

#### `search_games(query: str, client: BggClientProtocol) -> list[GameSummary]`

Search BGG for board games matching `query`. Returns results in BGG API order.
Returns an empty list when no games match.

#### `get_game(game_id: int, client: BggClientProtocol) -> GameDetails`

Fetch full details for the game identified by `game_id`.
Raises `BggNotFoundError` when the ID does not exist on BGG.

### `BggClientProtocol`

A `typing.Protocol` defining the client contract. Pass any object that implements
`search(query: str) -> list[GameSummary]` and `get_game(game_id: int) -> GameDetails`.
The bundled `BggClient` satisfies this protocol.

```python
from bgg_search import BggClient
client = BggClient(token="<your-token>")
```

### Models

#### `GameSummary`

| Field | Type  | Description         |
|-------|-------|---------------------|
| `id`  | `int` | BGG game ID         |
| `name`| `str` | Primary game title  |

#### `GameDetails`

| Field            | Type            | Description                        |
|------------------|-----------------|------------------------------------|
| `id`             | `int`           | BGG game ID                        |
| `name`           | `str`           | Primary game title                 |
| `year_published` | `int \| None`   | Year of first publication          |
| `min_players`    | `int \| None`   | Minimum number of players          |
| `max_players`    | `int \| None`   | Maximum number of players          |
| `min_playtime`   | `int \| None`   | Minimum play time in minutes       |
| `max_playtime`   | `int \| None`   | Maximum play time in minutes       |
| `weight`         | `float \| None` | BGG complexity weight (1.0 – 5.0)  |
| `bgg_rating`     | `float \| None` | BGG community rating (1.0 – 10.0)  |

### Exceptions

| Exception        | Inherits from    | Raised when                                |
|------------------|------------------|--------------------------------------------|
| `BggSearchError` | `Exception`      | Base class for all package exceptions      |
| `BggApiError`    | `BggSearchError` | BGG API returns an HTTP error              |
| `BggNotFoundError` | `BggSearchError` | Requested game ID does not exist         |
| `BggParseError`  | `BggSearchError` | BGG API response cannot be parsed         |

## CLI reference

All commands read the BGG token from the `BGG_TOKEN` environment variable and exit
with code 1 (printing an error to stderr) if it is not set or if the BGG API returns
an error.

### `bgg-search search <query>`

Search for board games by name.

```text
bgg-search search <query>
```

| Argument | Description          |
|----------|----------------------|
| `query`  | Free-text search term |

Output: one line per result, formatted as `{id:>8}  {name}`. No output when no games match.

### `bgg-search details <id>`

Fetch and display full details for a game.

```text
bgg-search details <id>
```

| Argument | Description |
|----------|-------------|
| `id`     | BGG game ID (integer) |

Output: labeled key-value block, one field per line:

```text
id:            13
name:          Catan
year:          1995
min_players:   3
max_players:   4
min_playtime:  60
max_playtime:  120
weight:        2.3
bgg_rating:    7.1
```

Exits with code 1 and prints an error to stderr when the game ID is not found.

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
