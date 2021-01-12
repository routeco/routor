from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def fixture_client(monkeypatch, graph_path: Path) -> TestClient:
    monkeypatch.setenv("map_path", str(graph_path))
    from routor.api.main import app  # late import to monkeypatch the settings

    client = TestClient(app)
    return client
