import os
import time

import pytest

from bgg_search._client import BggClient
from bgg_search.models import GameSummary

_CATAN_ID = 13


@pytest.fixture(scope="module")
def bgg_client() -> BggClient:
    token = os.getenv("BGG_TOKEN")
    if token is None:
        pytest.skip("BGG_TOKEN not set")
    return BggClient(token=token)


def test_search_returns_results(bgg_client: BggClient) -> None:
    results = bgg_client.search("Catan")
    time.sleep(2)

    assert len(results) > 0
    assert all(isinstance(r, GameSummary) for r in results)
    assert any(r.id == _CATAN_ID for r in results)
