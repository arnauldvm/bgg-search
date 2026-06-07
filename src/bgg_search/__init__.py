from importlib.metadata import version

from bgg_search._protocol import BggClientProtocol
from bgg_search.exceptions import BggApiError, BggNotFoundError, BggParseError, BggSearchError
from bgg_search.models import GameDetails, GameSummary

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
]
