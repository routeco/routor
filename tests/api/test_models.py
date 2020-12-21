import pytest
from pydantic import ValidationError

from routor import weights
from routor.api import models
from routor.models import Location

VALID_WEIGHTS = ["length", "travel_time"]


@pytest.mark.parametrize("weight", VALID_WEIGHTS)
def test_routerequest(mocker, weight: str) -> None:
    """
    Make sure a RouteRequest can be created.
    """
    mocker.patch.object(weights, "get_function_names", return_value=VALID_WEIGHTS)
    coordinate = Location(
        latitude=51.500427,
        longitude=-2.6741088,
    )

    models.RouteRequest(
        origin=coordinate,
        destination=coordinate,
        weight=weight,
    )


def test_routerequest__invalid_weight(mocker) -> None:
    """
    Make sure weight values are validated.
    """
    mocker.patch.object(weights, "get_function_names", return_value=VALID_WEIGHTS)
    coordinate = Location(
        latitude=51.500427,
        longitude=-2.6741088,
    )

    with pytest.raises(ValidationError):
        models.RouteRequest(
            origin=coordinate,
            destination=coordinate,
            weight="invalid_weight",
        )
