import os
import time

import pytest

from bgg_search._client import BggClient
from bgg_search._protocol import BggClientProtocol
from bgg_search.models import GameDetails, GameSummary
from bgg_search.search import search_games

_CATAN_ID = 13


@pytest.fixture(scope="module")
def client() -> BggClientProtocol:
    token = os.getenv("BGG_TOKEN")
    if token is None:
        pytest.skip("BGG_TOKEN not set")
    return BggClient(token=token)


def test_search_returns_results(client: BggClientProtocol) -> None:
    results = search_games("Catan", client)
    time.sleep(2)

    assert len(results) > 0
    assert all(isinstance(r, GameSummary) for r in results)
    assert any(r.id == _CATAN_ID for r in results)


def test_get_game_returns_details(bgg_client: BggClient) -> None:
    result = bgg_client.get_game(_CATAN_ID)
    time.sleep(2)

    assert isinstance(result, GameDetails)
    assert result.id == _CATAN_ID
    assert result.name == "Catan"
    assert result.year_published == 1995
    assert result.min_players is not None
    assert result.max_players is not None
    assert result.bgg_rating is not None
