from unittest.mock import MagicMock

import pytest

from bgg_search.models import GameSummary
from bgg_search.search import search_games


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
