import networkx
import pytest

from routor import exceptions, models

NODE_ID = 127498
EDGE_START_ID = NODE_ID
EDGE_END_ID = 305910


@pytest.mark.parametrize(
    ("lat_key", "lng_key"),
    (
        ("y", "x"),
        ("latitude", "longitude"),
    ),
)
def test_location(lat_key, lng_key) -> None:
    """
    Make sure we can initialise a location using aliases.
    """
    latitude = 51.500427
    longitude = -2.6741088

    location = models.Location(**{lat_key: latitude, lng_key: longitude})
    assert location.latitude == latitude
    assert location.longitude == longitude


def test_node__from_graph(graph: networkx.DiGraph) -> None:
    """
    Test node creation is working.
    """
    node_data = graph.nodes[NODE_ID]

    node = models.Node.from_graph(graph, NODE_ID)
    assert node.node_id == NODE_ID
    assert node.osm_id == node_data["osmid"]
    assert node.latitude == node_data["y"]
    assert node.longitude == node_data["x"]


def test_edge__from_graph(graph: networkx.DiGraph) -> None:
    """
    Test edge creation is working.
    """
    edge_data = graph[EDGE_START_ID][EDGE_END_ID][0]

    edge = models.Edge.from_graph(graph, EDGE_START_ID, EDGE_END_ID)
    assert edge.start == models.Node.from_graph(graph, EDGE_START_ID)
    assert edge.end == models.Node.from_graph(graph, EDGE_END_ID)
    assert edge.osm_id == edge_data["osmid"]
    assert edge.oneway is True
    assert edge.length == 61.516
    assert edge.travel_time == 2.0


def test_edge__from_graph__invalid_node(graph: networkx.DiGraph) -> None:
    """
    Raise proper exception if node is missing.
    """
    with pytest.raises(exceptions.NodeDoesNotExist):
        models.Edge.from_graph(graph, EDGE_START_ID, 0)

    with pytest.raises(exceptions.NodeDoesNotExist):
        models.Edge.from_graph(graph, 0, EDGE_END_ID)


def test_edge__from_nodes(graph: networkx.DiGraph) -> None:
    """
    Test edge creation is working.
    """
    edge_data = graph[EDGE_START_ID][EDGE_END_ID][0]
    start_node = models.Node.from_graph(graph, EDGE_START_ID)
    end_node = models.Node.from_graph(graph, EDGE_END_ID)

    edge = models.Edge.from_nodes(graph, start_node, end_node)
    assert edge.start == start_node
    assert edge.end == end_node
    assert edge.osm_id == edge_data["osmid"]
    assert edge.oneway is True
    assert edge.length == 61.516
    assert edge.travel_time == 2.0
