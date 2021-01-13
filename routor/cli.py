import json
import logging
from pathlib import Path

import click

from . import engine, models, weights
from .utils import graph as graph_utils
from .utils.click import LocationParamType

logging.basicConfig(level=logging.DEBUG)


@click.group()
def main():
    pass


@main.command()
@click.argument('location', type=str)
@click.argument('target', type=click.Path(exists=False, dir_okay=False))
@click.argument('as_oneways', type=bool, default=True)
def download(location: str, target: Path, as_oneways: bool) -> None:
    print(f"Download map for: {location}")
    graph = graph_utils.download_graph(location, as_oneways=as_oneways)
    graph_utils.save_graph(graph, target)
    print(f"Graph saved as {target}")


@main.command()
@click.argument('map_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('origin', type=LocationParamType())
@click.argument('destination', type=LocationParamType())
@click.argument('weight', type=click.Choice(weights.get_function_names()))
def route(
    map_path: Path, origin: models.Location, destination: models.Location, weight: str
) -> None:
    """
    Calculate a shortest path.

    \b
    MAP Path to an OSM file. Format: .osm.xml
    ORIGIN GPS location. Format: latitude,longitude
    DESTINATION GPS location. Format: latitude,longitude
    """
    data = engine.route(map_path, origin, destination, weight)

    print(json.dumps(data.dict(), indent=2))
