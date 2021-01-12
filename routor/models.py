from typing import Any, List

import networkx
from pydantic import BaseModel, Field, validator

from routor import exceptions


class Location(BaseModel):
    latitude: float  # alias: y
    longitude: float  # alias: x

    @validator("latitude")
    def validate_latitude(cls, value: float) -> float:  # noqa: N805
        if -90 > value or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validator("longitude")
    def validate_longitude(cls, value: float) -> float:  # noqa: N805
        if -180 > value or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value


class Node(Location):
    node_id: int
    osm_id: int = Field(alias="osmid")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_graph(cls, graph: networkx.Graph, node_id: int) -> "Node":
        try:
            node_data = graph.nodes[node_id]
        except KeyError as error:
            raise exceptions.NodeDoesNotExist() from error

        return cls(
            node_id=node_id,
            latitude=node_data["y"],
            longitude=node_data["x"],
            **node_data,
        )


class Edge(BaseModel):
    start: Node
    end: Node
    osm_id: int = Field(alias="osmid")
    oneway: bool
    length: float
    travel_time: float
    geometry: Any  # TODO

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def from_graph(cls, graph: networkx.Graph, start_id: int, end_id: int) -> "Edge":
        start = Node.from_graph(graph, start_id)
        end = Node.from_graph(graph, end_id)
        return Edge.from_nodes(graph, start, end)

    @classmethod
    def from_nodes(cls, graph: networkx.DiGraph, start: Node, end: Node) -> "Edge":
        try:
            edge_data = graph[start.node_id][end.node_id][0]
        except KeyError as error:
            raise exceptions.EdgeDoesNotExist() from error

        return cls(start=start, end=end, **edge_data)


class Route(BaseModel):
    costs: float
    length: float
    travel_time: float
    path: List[Location]
