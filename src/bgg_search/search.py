from bgg_search._protocol import BggClientProtocol
from bgg_search.models import GameSummary


def search_games(query: str, client: BggClientProtocol) -> list[GameSummary]:
    return client.search(query)
