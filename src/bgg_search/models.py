from dataclasses import dataclass


@dataclass(frozen=True)
class GameSummary:
    id: int
    name: str
