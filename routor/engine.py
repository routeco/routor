import logging
from pathlib import Path
from typing import Any, List, Optional, Tuple

import networkx
import osmnx
from more_itertools import pairwise
from networkx_astar_path import astar_path

from . import exceptions, models, weights
from .utils.debug import timeit
from .utils.graph import load_map

logger = logging.getLogger()


class Engine:
    graph: networkx.DiGraph

    @timeit
    def __init__(self, map_path: Path) -> None:
        logger.info("Initialise engine")
        self.graph = load_map(map_path)
        logger.info(
            f"Map loaded (edges: {len(self.graph.edges)}, nodes: {len(self.graph.nodes)})"
        )

    @timeit
    def find_path(
        self,
        origin: models.Node,
        destination: models.Node,
        weight: weights.WeightFunction,
    ) -> List[models.Node]:
        """
        Calculate a route using the given weight.
        """
        if origin.node_id not in self.graph.nodes:
            raise exceptions.NodeDoesNotExist(f"{origin} does not exists.")
        if origin.node_id not in self.graph.nodes:
            raise exceptions.NodeDoesNotExist(f"{origin} does not exists.")

        def _weight_wrapper(
            graph: networkx.DiGraph,
            prev_edge_nodes: Optional[Tuple[Any, Any]],
            edge_nodes: Tuple[Any, Any],
        ) -> float:
            prev_edge: Optional[models.Edge] = None
            if prev_edge_nodes:
                prev_edge = models.Edge.from_graph(self.graph, *prev_edge_nodes)
            edge = models.Edge.from_graph(self.graph, *edge_nodes)

            return weight(prev_edge, edge)

        logger.info(
            f"Calculating path from {origin.osm_id} to {destination.osm_id} with {weight}"
        )
        path = astar_path(
            self.graph, origin.node_id, destination.node_id, weight=_weight_wrapper
        )
        logger.info(f"Found path with {len(path)} items.")
        return [models.Node.from_graph(self.graph, node_id) for node_id in path]

    @timeit
    def route(
        self,
        origin: models.Location,
        destination: models.Location,
        weight_func: weights.WeightFunction,
        travel_time_func: weights.WeightFunction,
    ) -> models.Route:
        """
        Calculate a shortest path.
        """
        origin_node = self.get_closest_node(origin)
        destination_node = self.get_closest_node(destination)

        path = self.find_path(origin_node, destination_node, weight_func)
        costs = self.costs_for_path(path, weight_func)
        length = self.length_of_path(path)
        travel_time = self.travel_time_of_path(path, func=travel_time_func)

        route = models.Route(
            costs=round(costs, 2),
            length=round(length, 2),
            travel_time=round(travel_time, 2),
            path=[models.Location(**node.dict()) for node in path],
        )
        return route

    @timeit
    def costs_for_path(
        self, path: List[models.Node], func: weights.WeightFunction
    ) -> float:
        """
        Calculate the costs for a given path.
        """
        edges = (
            models.Edge.from_nodes(self.graph, start, end)
            for start, end in pairwise(path)
        )

        costs: float = 0
        for index, (prev_edge, edge) in enumerate(pairwise(edges)):
            if index == 0:
                costs = func(None, prev_edge)

            costs += func(prev_edge, edge)

        return costs

    @timeit
    def length_of_path(self, path: List[models.Node]) -> float:
        """
        Calculate the length of a given path.
        """
        edges = (
            models.Edge.from_nodes(self.graph, start, end)
            for start, end in pairwise(path)
        )

        return sum(edge.length for edge in edges)

    @timeit
    def travel_time_of_path(
        self, path: List[models.Node], func: weights.WeightFunction
    ) -> float:
        """
        Calculate the travel time of a given path.
        """
        return self.costs_for_path(path, func)

    @timeit
    def get_closest_node(self, location: models.Location) -> models.Node:
        """
        Get the closest node to a GPS location.
        """
        node_id = osmnx.get_nearest_node(
            self.graph, (location.latitude, location.longitude)
        )
        node = models.Node.from_graph(self.graph, node_id)
        logger.info(f"Found closest node for {location} is {node.osm_id}")
        return node
