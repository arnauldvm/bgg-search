from dataclasses import FrozenInstanceError

import pytest

from bgg_search.models import GameDetails, GameSummary


def test_game_summary_fields() -> None:
    game = GameSummary(id=1, name="Catan")
    assert game.id == 1
    assert game.name == "Catan"


def test_game_summary_immutable() -> None:
    game = GameSummary(id=1, name="Catan")
    with pytest.raises(FrozenInstanceError):
        game.id = 2  # type: ignore[misc]


def test_game_details_fields() -> None:
    game = GameDetails(
        id=13,
        name="Pandemic",
        year_published=2008,
        min_players=2,
        max_players=4,
        min_playtime=45,
        max_playtime=45,
        weight=2.41,
        bgg_rating=7.6,
    )
    assert game.id == 13
    assert game.name == "Pandemic"
    assert game.year_published == 2008
    assert game.min_players == 2
    assert game.max_players == 4
    assert game.min_playtime == 45
    assert game.max_playtime == 45
    assert game.weight == 2.41
    assert game.bgg_rating == 7.6


def test_game_details_nullable_fields() -> None:
    game = GameDetails(
        id=13,
        name="Pandemic",
        year_published=None,
        min_players=None,
        max_players=None,
        min_playtime=None,
        max_playtime=None,
        weight=None,
        bgg_rating=None,
    )
    assert game.year_published is None
    assert game.weight is None


def test_game_details_immutable() -> None:
    game = GameDetails(
        id=13,
        name="Pandemic",
        year_published=None,
        min_players=None,
        max_players=None,
        min_playtime=None,
        max_playtime=None,
        weight=None,
        bgg_rating=None,
    )
    with pytest.raises(FrozenInstanceError):
        game.id = 99  # type: ignore[misc]
