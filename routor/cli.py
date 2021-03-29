import json
import logging
from pathlib import Path
from typing import Optional, Tuple

import click

from . import models
from .engine import Engine
from .utils import click as click_utils
from .utils import core as core_utils
from .utils import graph as graph_utils


def set_log_level(log_level: Optional[str]) -> None:
    if log_level:
        level = getattr(logging, log_level)
        logging.basicConfig(level=level)


@click.group()
def main() -> None:
    pass


@main.command()
@click.option('--log-level', type=click.Choice(["INFO", "DEBUG"]), default="INFO")
@click.option(
    '--api-key',
    type=str,
    default=None,
    help="Google API key to add elevation to nodes and grades to edges.",
)
@click.option(
    '-n', '--node-tags', multiple=True, type=str, help="Additional node tags to fetch."
)
@click.option(
    '-e', '--edge-tags', multiple=True, type=str, help="Additional edge tags to fetch."
)
@click.argument('regions', nargs=-1, type=str)
@click.argument('target', type=click_utils.Path(exists=False, dir_okay=False))
def download(
    regions: Tuple[str],
    target: Path,
    log_level: Optional[str],
    node_tags: Tuple[str],
    edge_tags: Tuple[str],
    api_key: Optional[str] = None,
) -> None:
    """
    Download a compatible map.
    """
    set_log_level(log_level)

    graph = graph_utils.download_map(
        list(regions),
        node_tags=list(node_tags),
        edge_tags=list(edge_tags),
        api_key=api_key,
    )
    graph_utils.save_map(graph, target)


@main.command()
@click.option('--log-level', type=click.Choice(["INFO", "DEBUG"]), default="INFO")
@click.argument('map_path', type=click_utils.Path(exists=True, dir_okay=False))
@click.argument('origin', type=click_utils.LocationParamType())
@click.argument('destination', type=click_utils.LocationParamType())
@click.argument('weight', type=str)
@click.argument('travel_time', type=str)
def route(
    map_path: Path,
    origin: models.Location,
    destination: models.Location,
    weight: str,
    travel_time: str,
    log_level: Optional[str],
) -> None:
    """
    Calculate a shortest path.

    \b
    MAP Path to an OSM graphml file. Format: .graphml
    ORIGIN GPS location. Format: latitude,longitude
    DESTINATION GPS location. Format: latitude,longitude
    WEIGHT Module path to weight function, eg. "routor.weights.length"
    TRAVEL_TIME Module path to weight function, which returns the travel time for an edge, eg. "routor.weights.travel_time"
    """
    set_log_level(log_level)

    # load weight functions
    weight_func = core_utils.import_weight_function(weight)
    travel_time_func = core_utils.import_weight_function(travel_time)

    # do routing
    engine = Engine(map_path)
    data = engine.route(origin, destination, weight_func, travel_time_func)

    print(json.dumps(data.dict(), indent=2))
