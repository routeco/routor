import json
from pathlib import Path

import click

from . import models, weights
from .engine import Engine
from .utils.click import LocationParamType


@click.command()
@click.argument('map_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('origin', type=LocationParamType())
@click.argument('destination', type=LocationParamType())
@click.argument('weight', type=click.Choice(weights.get_function_names()))
def main(
    map_path: Path, origin: models.Location, destination: models.Location, weight: str
) -> None:
    """
    Calculate a shortest path.

    \b
    MAP Path to an OSM file. Format: .osm.xml
    ORIGIN GPS location. Format: latitude,longitude
    DESTINATION GPS location. Format: latitude,longitude
    """
    weight_func = getattr(weights, weight)

    engine = Engine(map_path)
    origin_node = engine.get_closest_node(origin)
    destination_node = engine.get_closest_node(destination)

    path = engine.route(origin_node, destination_node, weight=weight_func)
    costs = engine.costs_for_path(path, weight=weight_func)
    length = engine.length_of_path(path)
    travel_time = engine.travel_time_of_path(path)

    data = {
        "costs": round(costs, 2),
        "length": round(length, 2),
        "travel_time": round(travel_time, 2),
        "path": [(node.latitude, node.longitude) for node in path],
    }

    print(json.dumps(data, indent=2))
