from dataclasses import dataclass


@dataclass(frozen=True)
class GameSummary:
    """A board game entry returned from a BGG search."""

    id: int
    """BGG game ID."""
    name: str
    """Primary game title."""


@dataclass(frozen=True)
class GameDetails:
    """Full details for a board game retrieved from BGG."""

    id: int
    """BGG game ID."""
    name: str
    """Primary game title."""
    year_published: int | None
    """Year of first publication, or ``None`` if unknown."""
    min_players: int | None
    """Minimum number of players, or ``None`` if unknown."""
    max_players: int | None
    """Maximum number of players, or ``None`` if unknown."""
    min_playtime: int | None
    """Minimum play time in minutes, or ``None`` if unknown."""
    max_playtime: int | None
    """Maximum play time in minutes, or ``None`` if unknown."""
    weight: float | None
    """BGG complexity weight on a 1.0–5.0 scale, or ``None`` if unrated."""
    bgg_rating: float | None
    """BGG community rating on a 1.0–10.0 scale, or ``None`` if unrated."""
