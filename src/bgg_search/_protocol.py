from typing import Protocol, runtime_checkable

from bgg_search.models import GameDetails, GameSummary


@runtime_checkable
class BggClientProtocol(Protocol):
    """Contract for BGG API client implementations.

    Pass any conforming object to `search_games` or `get_game`.
    The bundled `BggClient` satisfies this protocol.
    """

    def search(self, query: str) -> list[GameSummary]:
        """Search BGG for board games matching `query`.

        Returns results in BGG API order; returns an empty list when no games match.
        """
        ...

    def get_game(self, game_id: int) -> GameDetails:
        """Fetch full details for the game identified by `game_id`.

        Raises `BggNotFoundError` when the ID does not exist on BGG.
        """
        ...
