import argparse
import os
import sys

from bgg_search._client import BggClient
from bgg_search.exceptions import BggSearchError
from bgg_search.search import search_games


def _get_client() -> BggClient:
    token = os.getenv("BGG_TOKEN")
    if not token:
        print("Error: BGG_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return BggClient(token=token)


def _search(args: argparse.Namespace) -> None:
    try:
        results = search_games(args.query, _get_client())
    except BggSearchError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    for game in results:
        print(f"{game.id:>8}  {game.name}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bgg-search",
        description="Search and inspect board games on BoardGameGeek.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    search_parser = subparsers.add_parser("search", help="Search games by name.")
    search_parser.add_argument("query", help="Search query string.")
    search_parser.set_defaults(func=_search)

    details_parser = subparsers.add_parser("details", help="Show full details for a game.")
    details_parser.add_argument("id", type=int, help="BGG game ID.")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    args.func(args)
