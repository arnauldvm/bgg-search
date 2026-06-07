from typing import Protocol, runtime_checkable

from bgg_search.models import GameDetails, GameSummary


@runtime_checkable
class BggClientProtocol(Protocol):
    def search(self, query: str) -> list[GameSummary]: ...
    def get_game(self, game_id: int) -> GameDetails: ...
