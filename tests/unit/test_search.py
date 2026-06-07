from unittest.mock import MagicMock

import pytest

from bgg_search.exceptions import BggNotFoundError
from bgg_search.models import GameDetails, GameSummary
from bgg_search.search import get_game, search_games


@pytest.fixture
def mock_client() -> MagicMock:
    return MagicMock()


def test_search_games_delegates_to_client(mock_client: MagicMock) -> None:
    expected = [GameSummary(id=1, name="Catan")]
    mock_client.search.return_value = expected

    result = search_games("Catan", mock_client)

    mock_client.search.assert_called_once_with("Catan")
    assert result == expected


def test_search_games_returns_empty_list(mock_client: MagicMock) -> None:
    mock_client.search.return_value = []

    result = search_games("unknown", mock_client)

    assert result == []


def test_get_game_delegates_to_client(mock_client: MagicMock) -> None:
    expected = GameDetails(
        id=13,
        name="Catan",
        year_published=1995,
        min_players=3,
        max_players=4,
        min_playtime=60,
        max_playtime=120,
        weight=2.3,
        bgg_rating=7.1,
    )
    mock_client.get_game.return_value = expected

    result = get_game(13, mock_client)

    mock_client.get_game.assert_called_once_with(13)
    assert result == expected


def test_get_game_propagates_not_found(mock_client: MagicMock) -> None:
    mock_client.get_game.side_effect = BggNotFoundError("not found")

    with pytest.raises(BggNotFoundError):
        get_game(999, mock_client)
