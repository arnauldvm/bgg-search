from bgg_search._protocol import BggClientProtocol
from bgg_search.models import GameDetails, GameSummary


def search_games(query: str, client: BggClientProtocol) -> list[GameSummary]:
    return client.search(query)


def get_game(game_id: int, client: BggClientProtocol) -> GameDetails:
    return client.get_game(game_id)
