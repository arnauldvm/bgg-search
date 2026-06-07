import time

from bgg_search._client import BggClient
from bgg_search.models import GameSummary

_CATAN_ID = 13


def test_search_returns_results() -> None:
    client = BggClient()
    results = client.search("Catan")
    time.sleep(2)

    assert len(results) > 0
    assert all(isinstance(r, GameSummary) for r in results)
    assert any(r.id == _CATAN_ID for r in results)
