from pathlib import Path

import networkx
import osmnx
import pytest

from routor.utils import graph as graph_utils


def test_load_map(graph_path: Path, graph: networkx.Graph) -> None:
    """
    Make sure graph is loaded unchanged.
    """
    expected_graph = graph
    graph = graph_utils.load_map(graph_path)
    assert list(graph.nodes) == list(expected_graph.nodes)
    assert list(graph.edges) == list(expected_graph.edges)


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr
def test_download_graph() -> None:
    """
    Make sure we can download a map.
    """
    graph = graph_utils.download_graph("Nailsea, North Somerset, England")
    assert isinstance(graph, networkx.DiGraph)

    # make sure some specific attributes/tags are available
    nodes, edges = osmnx.utils_graph.graph_to_gdfs(graph)
    assert not {
        "osmid",
        "highway",
        "name",
        "maxspeed",
        "length",
        "oneway",
        "bearing",
        "speed_kph",
        "travel_time",
    }.difference(edges.columns.tolist())
    assert not {"y", "x", "highway", "street_count"}.difference(nodes.columns.tolist())


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr
@pytest.mark.parametrize("tag", ["crossing", "traffic_calming"])
def test_download_graph__custom_node_tags(tag: str) -> None:
    """
    Make sure additional node tags have been fetched.
    """
    graph = graph_utils.download_graph(
        "Nailsea, North Somerset, England", node_tags=[tag]
    )
    nodes, _ = osmnx.utils_graph.graph_to_gdfs(graph)
    assert tag in nodes.columns.tolist()


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr
@pytest.mark.parametrize("tag", ["surface"])
def test_download_graph__custom_edge_tags(tag: str) -> None:
    """
    Make sure additional node tags have been fetched.
    """
    graph = graph_utils.download_graph(
        "Nailsea, North Somerset, England", edge_tags=[tag]
    )
    _, edges = osmnx.utils_graph.graph_to_gdfs(graph)
    assert tag in edges.columns.tolist()
