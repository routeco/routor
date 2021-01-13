import copy
import logging
from pathlib import Path
from typing import Tuple

import networkx
import osmnx
from osmnx.graph import graph_from_xml

from .debug import timeit

logger = logging.getLogger()


@timeit
def load_map(map_path: Path) -> networkx.DiGraph:
    """
    Load graph from a .osm.xml file.
    """
    graph = graph_from_xml(
        map_path, bidirectional=False, simplify=False, retain_all=False
    )
    return graph


def is_oneway(edge: Tuple[int, int, dict]) -> bool:
    """
    Return whether edge is a oneway.
    """
    _, _, data = edge
    return data.get('oneway', False) == 'yes'


def is_twoway(edge: Tuple[int, int, dict]) -> bool:
    """
    Return whether edge is a two way.
    """
    return not is_oneway(edge)


@timeit
def convert_to_oneways(graph: networkx.DiGraph) -> networkx.DiGraph:
    """
    Convert all two ways to two one ways and reset osmids.
    """
    logger.info("Converting two ways to one ways")
    graph = graph.copy()  # create a new graph

    # rewrite osmid
    all_edges = graph.edges(data=True)
    twoways = list(filter(is_twoway, all_edges))

    # convert all ways to one ways and reset the osmid
    new_osmid = 0
    for new_osmid, (_, _, edge_data) in enumerate(all_edges):
        edge_data['original_osmid'] = edge_data['osmid']
        edge_data['osmid'] = new_osmid
        edge_data['oneway'] = True

    # add reverse edge for two ways
    for osmid, (u, v, original_data) in enumerate(twoways, start=new_osmid + 1):
        edge_data = copy.deepcopy(original_data)
        edge_data['osmid'] = osmid
        graph.add_edge(v, u, **edge_data)

    # make sure we only have unique edge ids
    edge_ids = []
    for _, _, edge_data in graph.edges(data=True):
        edge_ids.append(edge_data['osmid'])

    if len(edge_ids) != len(set(edge_ids)):
        raise RuntimeError("Duplicate edges found.")

    return graph


@timeit
def download_graph(location: str, as_oneways: bool = False) -> networkx.DiGraph:
    logger.info(f"Download map for {location}")
    osmnx.utils.config(all_oneway=True)

    graph = osmnx.graph_from_place(
        location,
        network_type="drive",
        retain_all=False,  # only keep biggest connected network
        truncate_by_edge=True,  # Keep entirety of edges, rather than cropping at distance limit
        simplify=False,  # Do not correct and simplify street network topology
    )

    if as_oneways:
        return convert_to_oneways(graph)
    return graph


@timeit
def save_graph(graph: networkx.DiGraph, target: Path) -> None:
    """
    Save graph as .osm.xml file.
    """
    logger.info("Saving graph as {target}.")
    osmnx.save_graph_xml(
        graph,
        filepath=str(target),
        merge_edges=False,
    )
