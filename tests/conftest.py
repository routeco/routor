from pathlib import Path

import osmnx
import pytest
from networkx import DiGraph

from routor.engine import Engine


@pytest.fixture()
def graph_path() -> Path:
    """
    Return path to a test .osm.xml file.
    """
    test_dir = Path(__file__).parent
    return test_dir / "tiny_bristol.graphml"


@pytest.fixture
def graph(graph_path: Path) -> DiGraph:
    """
    Return a graph for testing.
    """
    graph = osmnx.io.load_graphml(
        str(graph_path),
    )
    return graph


@pytest.fixture
def engine(graph_path: Path) -> Engine:
    """
    Return a routing engine.
    """
    return Engine(graph_path)
