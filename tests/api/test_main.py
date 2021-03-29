import pytest
from fastapi.testclient import TestClient

from routor import engine, models, weights


def test_read_weights(mocker, client: TestClient) -> None:
    """
    Test that availale weight functions are returned.
    """
    expected_weights = ["time_travel", "length"]
    mocker.patch.object(weights, "get_function_names", return_value=expected_weights)

    response = client.get("/weights")
    assert response.status_code == 200
    assert response.json() == expected_weights


@pytest.mark.parametrize(("weight", "weight_func"), weights.WEIGHT_FUNCTIONS.items())
def test_read_route(
    mocker,
    client: TestClient,
    weight: str,
    weight_func: weights.WeightFunction,
) -> None:
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
    mocker.patch.object(
        engine.Engine, "route", return_value=models.Route(**expected_data)
    )

    response = client.get(
        "/route",
        json={
            "origin": origin.dict(),
            "destination": destination.dict(),
            "weight": weight,
        },
    )
    assert response.status_code == 200, response.content
    engine.Engine.route.assert_called_with(origin, destination, weight_func, weights.travel_time)  # type: ignore
    assert response.json() == expected_data
