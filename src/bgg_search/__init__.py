from importlib.metadata import version

from bgg_search._protocol import BggClientProtocol
from bgg_search.exceptions import BggApiError, BggNotFoundError, BggParseError, BggSearchError
from bgg_search.models import GameDetails, GameSummary
from bgg_search.search import get_game, search_games

__version__ = version("bgg-search")

__all__ = [
    "__version__",
    "BggClientProtocol",
    "BggApiError",
    "BggNotFoundError",
    "BggParseError",
    "BggSearchError",
    "GameDetails",
    "GameSummary",
    "get_game",
    "search_games",
]
