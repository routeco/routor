import networkx
import pytest

from routor import models, weights

NODE_ID = 127498
EDGE_START_ID = NODE_ID
EDGE_END_ID = 305910


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
