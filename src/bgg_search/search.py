from bgg_search._protocol import BggClientProtocol
from bgg_search.models import GameDetails, GameSummary


def search_games(query: str, client: BggClientProtocol) -> list[GameSummary]:
    """Search BGG for board games matching `query` using `client`.

    Returns results in BGG API order; returns an empty list when no games match.
    """
    return client.search(query)


def get_game(game_id: int, client: BggClientProtocol) -> GameDetails:
    """Fetch full details for the game identified by `game_id` using `client`.

    Raises `BggNotFoundError` when the ID does not exist on BGG.
    """
    return client.get_game(game_id)
