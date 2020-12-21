from pathlib import Path

import networkx

from routor.utils import graph as graph_utils


def test_load_map(graph_path: Path, graph: networkx.Graph) -> None:
    """
    Make sure graph is loaded unchanged.
    """
    expected_graph = graph
    graph = graph_utils.load_map(graph_path)
    assert list(graph.nodes) == list(expected_graph.nodes)
    assert list(graph.edges) == list(expected_graph.edges)
