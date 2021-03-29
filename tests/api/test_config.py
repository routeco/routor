import pytest

from routor.api.config import Settings
from routor.weights import travel_time


def test_validate_default_path() -> None:
    """
    Make sure the module path is validated
    """
    with pytest.raises(AttributeError):
        Settings(map_path="...", travel_time_func="routor.weights.travel_time_123")


def test_get_travel_time_func() -> None:
    """
    Make sure travel_time func is imported correctly.
    """
    settings = Settings(map_path="...", travel_time_func="routor.weights.travel_time")
    assert settings.get_travel_time_func() == travel_time
