from pathlib import Path

import osmnx
import pytest
from networkx import DiGraph
from osmnx.graph import graph_from_xml

from routor.engine import Engine


@pytest.fixture()
def graph_path() -> Path:
    """
    Return path to a test .osm.xml file.
    """
    test_dir = Path(__file__).parent
    return test_dir / "tiny_bristol.osm.xml"


@pytest.fixture
def graph(graph_path: Path) -> DiGraph:
    """
    Return a graph for testing.
    """
    graph = graph_from_xml(
        str(graph_path), bidirectional=False, simplify=False, retain_all=False
    )
    osmnx.add_edge_bearings(graph)
    osmnx.add_edge_speeds(graph)
    osmnx.add_edge_travel_times(graph)
    return graph


@pytest.fixture
def engine(graph_path: Path) -> Engine:
    """
    Return a routing engine.
    """
    return Engine(graph_path)
