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
    Prepare osmnx config for downloading data.
    """
    # aggregate default tags
    useful_node_tags = set(
        osmnx.settings.useful_tags_node
        + osmnx.settings.osm_xml_node_attrs
        + osmnx.settings.osm_xml_node_tags
        + ["junction"]  # additional useful tags
        + ["street_count"]  # custom enhancements
        + node_tags
    )
    useful_edge_tags = set(
        osmnx.settings.useful_tags_way
        + osmnx.settings.osm_xml_way_attrs
        + osmnx.settings.osm_xml_way_tags
        + ["junction"]  # additional useful tags
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
def tag_roundabout_nodes(graph: networkx.DiGraph) -> None:
    """
    Tag nodes within a roundabout as junction=roundabout.

    Not every node within a roundabout is always tagged accordingly. Let's fix that.
    More information:
    * https://wiki.openstreetmap.org/wiki/Key:junction
    * https://wiki.openstreetmap.org/wiki/Tag:junction%3Droundabout
    """
    for u, v, edge_data in graph.edges(data=True):
        if edge_data.get("junction", None) != "roundabout":
            continue

        for node_id in (u, v):
            node_data = graph.nodes[node_id]
            if node_data.get("junction", None) == "circular":
                # no need to do anything as this is a "roundabout"
                # https://wiki.openstreetmap.org/wiki/Tag:junction%3Dcircular?
                continue

            if "junction" in node_data and node_data["junction"] != "roundabout":
                logger.warning(
                    "Node %s was already tagged with `junction='%s'`.",
                    node_id,
                    node_data["junction"],
                )
            node_data["junction"] = "roundabout"


@timeit
def download_graph(
    location: str,
    node_tags: Optional[List[str]] = None,
    edge_tags: Optional[List[str]] = None,
    api_key: Optional[str] = None,
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
    logger.info("> Tag node as roundabout")
    tag_roundabout_nodes(graph)

    logger.info("> Adding street count to nodes")
    street_count_data = osmnx.utils_graph.count_streets_per_node(graph)
    for node_id, street_count in street_count_data.items():
        graph.nodes[node_id]["street_count"] = street_count

    if api_key:
        logger.info("> Adding elevation")
        osmnx.add_node_elevations(graph, api_key, precision=5)

        logger.info("> Add edge grades")
        osmnx.elevation.add_edge_grades(graph)

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
    logger.info(f"Saving graph as {target.absolute()}.")
    osmnx.save_graphml(
        graph,
        filepath=str(target),
    )
