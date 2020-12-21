from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

import networkx
import osmnx
from more_itertools import pairwise
from networkx_astar_path import astar_path

from . import exceptions, models
from .utils.graph import load_map

WeightFunction = Callable[[Optional[models.Edge], models.Edge], float]


class Engine:
    graph: networkx.DiGraph

    def __init__(self, map: Path) -> None:
        self.graph = load_map(map)

        # add additional attributes
        osmnx.bearing.add_edge_bearings(self.graph)
        osmnx.speed.add_edge_speeds(self.graph, hwy_speeds=None, fallback=30)
        osmnx.speed.add_edge_travel_times(self.graph)

    def route(
        self, origin: models.Node, destination: models.Node, weight: WeightFunction
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

        path = astar_path(
            self.graph, origin.node_id, destination.node_id, weight=_weight_wrapper
        )
        return [models.Node.from_graph(self.graph, node_id) for node_id in path]

    def costs_for_path(self, path: List[models.Node], weight: WeightFunction) -> float:
        """
        Calculate the costs for a given path.
        """
        edges = (
            models.Edge.from_nodes(self.graph, start, end)
            for start, end in pairwise(path)
        )

        costs: float = None  # type: ignore
        for prev_edge, edge in pairwise(edges):
            if costs is None:
                costs = weight(None, prev_edge)

            costs += weight(prev_edge, edge)

        return costs

    def length_of_path(self, path: List[models.Node]) -> float:
        """
        Calculate the length of a given path.
        """
        edges = (
            models.Edge.from_nodes(self.graph, start, end)
            for start, end in pairwise(path)
        )

        return sum(edge.length for edge in edges)

    def travel_time_of_path(self, path: List[models.Node]) -> float:
        """
        Calculate the travel time of a given path.
        """
        edges = (
            models.Edge.from_nodes(self.graph, start, end)
            for start, end in pairwise(path)
        )

        return sum(edge.travel_time for edge in edges)

    def get_closest_node(self, location: models.Location) -> models.Node:
        """
        Get the closest node to a GPS location.
        """
        node_id = osmnx.get_nearest_node(
            self.graph, (location.latitude, location.longitude)
        )
        return models.Node.from_graph(self.graph, node_id)
