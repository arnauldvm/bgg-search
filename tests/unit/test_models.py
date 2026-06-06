from dataclasses import FrozenInstanceError

import pytest

from bgg_search.models import GameSummary


def test_game_summary_fields() -> None:
    game = GameSummary(id=1, name="Catan")
    assert game.id == 1
    assert game.name == "Catan"


def test_game_summary_immutable() -> None:
    game = GameSummary(id=1, name="Catan")
    with pytest.raises(FrozenInstanceError):
        game.id = 2  # type: ignore[misc]
