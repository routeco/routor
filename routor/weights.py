from functools import partial
from typing import Optional

from . import models

__all__ = ["travel_time", "length"]


def weight_by_attr(
    attr: str, prev_edge: Optional[models.Edge], edge: models.Edge
) -> float:
    """
    Generic weight function to retrieve a value from an edge.
    """
    return getattr(edge, attr)


travel_time = partial(weight_by_attr, "travel_time")
length = partial(weight_by_attr, "length")
