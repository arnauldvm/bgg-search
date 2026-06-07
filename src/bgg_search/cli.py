import argparse


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bgg-search",
        description="Search and inspect board games on BoardGameGeek.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    search_parser = subparsers.add_parser("search", help="Search games by name.")
    search_parser.add_argument("query", help="Search query string.")

    details_parser = subparsers.add_parser("details", help="Show full details for a game.")
    details_parser.add_argument("id", type=int, help="BGG game ID.")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    args.func(args)
