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


def test_tag_roundabout_nodes() -> None:
    """
    Make sure nodes are tagged as roundabout as well.
    """
    graph = networkx.DiGraph()
    graph.add_edge(0, 1)  # go in
    graph.add_edge(1, 2, junction="roundabout")  # roundabout
    graph.add_edge(2, 3, junction="roundabout")  # roundabout
    graph.add_edge(3, 1, junction="roundabout")  # roundabout
    graph.add_edge(2, 4)  # get out

    graph_utils.tag_roundabout_nodes(graph)

    assert graph.nodes[0] == {}
    assert graph.nodes[4] == {}
    # everything else is part of the roundabout
    assert graph.nodes[1] == {"junction": "roundabout"}
    assert graph.nodes[2] == {"junction": "roundabout"}
    assert graph.nodes[3] == {"junction": "roundabout"}


def test_tag_roundabout_nodes__keep_circular() -> None:
    """
    Make sure nodes tagged with junction=circular are not retagged.
    """
    graph = networkx.DiGraph()
    graph.add_node(1, junction="circular")
    graph.add_node(2, junction="circular")
    graph.add_node(3, junction="circular")

    graph.add_edge(0, 1)  # go in
    graph.add_edge(1, 2, junction="roundabout")  # roundabout
    graph.add_edge(2, 3, junction="roundabout")  # roundabout
    graph.add_edge(3, 1, junction="roundabout")  # roundabout
    graph.add_edge(2, 4)  # get out

    graph_utils.tag_roundabout_nodes(graph)

    assert graph.nodes[0] == {}
    assert graph.nodes[4] == {}
    # do not overwrite junction type circular
    assert graph.nodes[1] == {"junction": "circular"}
    assert graph.nodes[2] == {"junction": "circular"}
    assert graph.nodes[3] == {"junction": "circular"}


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr
def test_download_map() -> None:
    """
    Make sure we can download a map.
    """
    graph = graph_utils.download_map("Nailsea, North Somerset, England")
    assert isinstance(graph, networkx.DiGraph)

    # make sure some specific attributes/tags are available
    nodes, edges = osmnx.utils_graph.graph_to_gdfs(graph)
    assert not {
        "osmid",
        "highway",
        "name",
        "maxspeed",
        "length",
        "junction",
        "oneway",
        "bearing",
        "speed_kph",
        "travel_time",
    }.difference(edges.columns.tolist())
    assert not {"y", "x", "highway", "junction", "street_count"}.difference(
        nodes.columns.tolist()
    )


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr
@pytest.mark.parametrize("tag", ["crossing", "traffic_calming"])
def test_download_graph__custom_node_tags(tag: str) -> None:
    """
    Make sure additional node tags have been fetched.
    """
    graph = graph_utils.download_map(
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
    graph = graph_utils.download_map(
        "Nailsea, North Somerset, England", edge_tags=[tag]
    )
    _, edges = osmnx.utils_graph.graph_to_gdfs(graph)
    assert tag in edges.columns.tolist()


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr("download_nailsea_elevation.yaml")
def test_download_graph__add_elevation() -> None:
    """
    Make sure elevation is attached once an Google API key has been provided.
    """
    graph = graph_utils.download_map(
        "Nailsea, North Somerset, England", api_key="some_random_api_key"
    )
    nodes, _ = osmnx.utils_graph.graph_to_gdfs(graph)
    assert "elevation" in nodes.columns.tolist()


@pytest.mark.default_cassette("download_nailsea.yaml")
@pytest.mark.vcr("download_nailsea_elevation.yaml")
def test_download_graph__add_grades() -> None:
    """
    Make sure grades are attached once an Google API key has been provided.
    """
    graph = graph_utils.download_map(
        "Nailsea, North Somerset, England", api_key="some_random_api_key"
    )
    _, edges = osmnx.utils_graph.graph_to_gdfs(graph)
    assert "grade" in edges.columns.tolist()
