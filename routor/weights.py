from functools import partial
from typing import Callable, Dict, List, Optional

from . import models

WeightFunction = Callable[[Optional[models.Edge], models.Edge], float]

WEIGHT_FUNCTIONS: Dict[str, WeightFunction] = {}


def register(func: WeightFunction, function_name: str) -> None:
    """
    Register a custom weight function.
    """
    if function_name in WEIGHT_FUNCTIONS:
        raise ValueError("Function with the same name is already registered.")
    WEIGHT_FUNCTIONS[function_name] = func


def unregister(function_name: str) -> None:
    """
    Unregister a custom weight function.
    """
    try:
        del WEIGHT_FUNCTIONS[function_name]
    except KeyError:
        pass


def get_function(name: str) -> WeightFunction:
    """
    Return the matching weight function.
    """
    try:
        return WEIGHT_FUNCTIONS[name.lower()]
    except KeyError as error:
        raise ValueError("Weight function does not exist.") from error


def get_function_names() -> List[str]:
    """
    Return list of possible weight functions.
    """
    return list(WEIGHT_FUNCTIONS.keys())


def weight_by_attr(
    attr: str, prev_edge: Optional[models.Edge], edge: models.Edge
) -> float:
    """
    Generic weight function to retrieve a value from an edge.
    """
    return getattr(edge, attr)


travel_time = partial(weight_by_attr, "travel_time")
register(travel_time, "travel_time")

length = partial(weight_by_attr, "length")
register(length, "length")
