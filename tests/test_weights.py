from functools import partial

import networkx
import pytest

from routor import models, weights

NODE_ID = 127498
EDGE_START_ID = NODE_ID
EDGE_END_ID = 305910


def test_get_function() -> None:
    """
    Make sure a registerd function can be retrieved by name.
    """
    assert weights.get_function('length') == weights.length


def test_get_function_names() -> None:
    """
    Make sure names for the registered functions are returned
    """
    assert weights.get_function_names() == ['travel_time', 'length']


def test_register() -> None:
    """
    Make sure new weight functions can be registered and unregistered.
    """
    my_weight = partial(weights.weight_by_attr, "my_weight")
    weights.register(my_weight, "my_weight")
    assert weights.get_function("my_weight")
    weights.unregister("my_weight")


@pytest.mark.parametrize(
    ("func_name", "expected_value"), (("travel_time", 2.0), ("length", 61.516))
)
def test_travel_time(
    graph: networkx.DiGraph, func_name: str, expected_value: float
) -> None:
    """
    Make sure attributes are retrieved correctly.
    """
    edge = models.Edge.from_graph(graph, EDGE_START_ID, EDGE_END_ID)
    method = getattr(weights, func_name)
    value = method(None, edge)
    assert value == expected_value
