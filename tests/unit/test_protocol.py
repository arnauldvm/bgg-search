from bgg_search._protocol import BggClientProtocol
from bgg_search.models import GameDetails, GameSummary


def test_conforming_class_is_instance() -> None:
    class ConformingClient:
        def search(self, query: str) -> list[GameSummary]:
            return []

        def get_game(self, game_id: int) -> GameDetails:
            return GameDetails(
                id=game_id,
                name="",
                year_published=None,
                min_players=None,
                max_players=None,
                min_playtime=None,
                max_playtime=None,
                weight=None,
                bgg_rating=None,
            )

    assert isinstance(ConformingClient(), BggClientProtocol)


def test_non_conforming_class_is_not_instance() -> None:
    class NonConforming:
        pass

    assert not isinstance(NonConforming(), BggClientProtocol)
