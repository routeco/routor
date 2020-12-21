import pytest
from fastapi.testclient import TestClient

from routor import engine, models, weights


@pytest.fixture(name="client")
def fixture_client(monkeypatch, graph_path: str) -> TestClient:
    monkeypatch.setenv("map_path", graph_path)
    from routor.api.views import app  # late import to monkeypatch the settings

    client = TestClient(app)
    return client


def test_read_version(client: TestClient) -> None:
    """
    Make sure the current app version is accessable.
    """
    response = client.get("/version")
    assert response.status_code == 200

    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)


def test_read_weights(mocker, client: TestClient) -> None:
    """
    Test that availale weight functions are returned.
    """
    expected_weights = ["time_travel", "length"]
    mocker.patch.object(weights, "get_function_names", return_value=expected_weights)

    response = client.get("/weights")
    assert response.status_code == 200
    assert response.json() == expected_weights


@pytest.mark.parametrize("weight", ("travel_time", "length"))
def test_read_route(mocker, graph_path: str, client: TestClient, weight: str) -> None:
    """
    Test if a proper route from A to B and its metadata is returned.
    """
    origin = models.Location(latitude=51.454514, longitude=-2.587910)
    destination = models.Location(latitude=52.520008, longitude=13.404954)
    expected_data = {
        "costs": 10,
        "length": 30,
        "travel_time": 20,
        "path": [
            {"latitude": 50, "longitude": -2},
            {"latitude": 50.1, "longitude": -2.1},
        ],
    }
    mocker.patch.object(engine, "route", return_value=models.Route(**expected_data))

    response = client.get(
        "/route",
        json={
            "origin": origin.dict(),
            "destination": destination.dict(),
            "weight": weight,
        },
    )
    assert response.status_code == 200, response.content
    engine.route.assert_called_with(graph_path, origin, destination, weight)  # type: ignore
    assert response.json() == expected_data
