import click
import pytest

from routor.utils import click as click_utils


def test_locationparamtype() -> None:
    """
    Make sure gps coordinates are parsed correctly.
    """
    value = "51.500427,-2.6741088"

    parser = click_utils.LocationParamType()
    location = parser.convert(value, None, None)
    assert location.latitude == 51.500427
    assert location.longitude == -2.6741088


@pytest.mark.parametrize(
    "value",
    (
        "51.500427 -2.6741088",
        "51.500427,-a.6741088",
    ),
)
def test_locationparamtype__invalid(value: str) -> None:
    """
    Invalid values should faile
    """
    parser = click_utils.LocationParamType()
    with pytest.raises(click.BadParameter):
        parser.convert(value, None, None)
