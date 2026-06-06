from dataclasses import dataclass


@dataclass(frozen=True)
class GameSummary:
    id: int
    name: str


@dataclass(frozen=True)
class GameDetails:
    id: int
    name: str
    year_published: int | None
    min_players: int | None
    max_players: int | None
    min_playtime: int | None
    max_playtime: int | None
    weight: float | None
    bgg_rating: float | None
