from pathlib import Path

import networkx
from osmnx.graph import graph_from_xml


def load_map(map_path: Path) -> networkx.DiGraph:
    """
    Load graph from a .osm.xml file.
    """
    graph = graph_from_xml(
        map_path, bidirectional=False, simplify=False, retain_all=False
    )
    return graph
