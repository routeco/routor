import contextlib
import logging
from pathlib import Path
from typing import Generator, List, Optional

import networkx
import osmnx

from .debug import timeit

logger = logging.getLogger()


@timeit
def load_map(map_path: Path) -> networkx.DiGraph:
    """
    Load graph from a .graphml file.
    """
    graph = osmnx.io.load_graphml(
        map_path,
    )
    return graph


@contextlib.contextmanager
def osmnx_config(
    node_tags: List[str], edge_tags: List[str]
) -> Generator[None, None, None]:
    """
    Prepare osmnx for downloading a data.
    """
    # aggregate default tags
    useful_node_tags = set(
        osmnx.settings.useful_tags_node
        + osmnx.settings.osm_xml_node_attrs
        + osmnx.settings.osm_xml_node_tags
        + ["street_count"]  # custom enhancements
        + node_tags
    )
    useful_edge_tags = set(
        osmnx.settings.useful_tags_way
        + osmnx.settings.osm_xml_way_attrs
        + osmnx.settings.osm_xml_way_tags
        + ["bearing", "speed_kph", "travel_time"]  # custom enhancements
        + edge_tags
    )

    original_settings = {
        "all_oneway": osmnx.settings.all_oneway,
        "useful_tags_node": osmnx.settings.useful_tags_node,
        "useful_tags_way": osmnx.settings.useful_tags_node,
    }
    new_settings = {
        "all_oneway": False,  # we need digraph, an edge for each direction
        "useful_tags_node": useful_node_tags,
        "useful_tags_way": useful_edge_tags,
    }
    try:
        logger.debug("Update osmnx configuration", extra=new_settings)
        osmnx.config(**new_settings)
        yield
    finally:
        logger.debug("Resetting osmnx configuration", extra=original_settings)
        osmnx.config(**original_settings)


@timeit
def download_graph(
    location: str,
    node_tags: Optional[List[str]] = None,
    edge_tags: Optional[List[str]] = None,
) -> networkx.DiGraph:
    """
    Download map from OSM.
    """
    logger.info(f"Download map for {location}")
    with osmnx_config(node_tags or [], edge_tags or []):
        graph = osmnx.graph_from_place(
            location,
            network_type="drive",
            retain_all=False,  # only keep biggest connected network
            truncate_by_edge=True,  # Keep entirety of edges, rather than cropping at distance limit
            simplify=False,  # Do not correct and simplify street network topology
        )

    # add additional attributes
    logger.info("Enhance map with additional attributes")
    logger.info("> Adding street count to nodes")
    for node_id, street_count in osmnx.utils_graph.count_streets_per_node(
        graph
    ).items():
        graph.nodes[node_id]["street_count"] = street_count
    logger.info("> Adding bearing")
    osmnx.bearing.add_edge_bearings(graph)
    logger.info("> Adding edge speeds")
    osmnx.speed.add_edge_speeds(graph, hwy_speeds=None, fallback=30)
    logger.info("> Adding travel time")
    osmnx.speed.add_edge_travel_times(graph)

    return graph


@timeit
def save_graph(graph: networkx.DiGraph, target: Path) -> None:
    """
    Save graph as .graphml file.
    """
    logger.info("Saving graph as {target}.")
    osmnx.save_graphml(
        graph,
        filepath=str(target),
    )
