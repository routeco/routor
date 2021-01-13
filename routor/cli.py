import json
import logging
from pathlib import Path
from typing import Optional

import click

from . import engine, models
from .utils import graph as graph_utils
from .utils.click import LocationParamType


def set_log_level(log_level: Optional[str]) -> None:
    if log_level:
        level = getattr(logging, log_level)
        logging.basicConfig(level=level)


@click.group()
def main() -> None:
    pass


@main.command()
@click.option('--log-level', type=click.Choice(["INFO", "DEBUG"]), default="INFO")
@click.argument('location', type=str)
@click.argument('target', type=click.Path(exists=False, dir_okay=False))
@click.argument('as_oneways', type=bool, default=True)
def download(
    location: str, target: Path, as_oneways: bool, log_level: Optional[str]
) -> None:
    """
    Download a compatible map.
    """
    set_log_level(log_level)

    print(f"Download map for: {location}")
    graph = graph_utils.download_graph(location, as_oneways=as_oneways)
    graph_utils.save_graph(graph, target)
    print(f"Graph saved as {target}")


@main.command()
@click.option('--log-level', type=click.Choice(["INFO", "DEBUG"]), default="INFO")
@click.argument('map_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('origin', type=LocationParamType())
@click.argument('destination', type=LocationParamType())
@click.argument('weight', type=str)
def route(
    map_path: Path,
    origin: models.Location,
    destination: models.Location,
    weight: str,
    log_level: Optional[str],
) -> None:
    """
    Calculate a shortest path.

    \b
    MAP Path to an OSM graphml file. Format: .graphml
    ORIGIN GPS location. Format: latitude,longitude
    DESTINATION GPS location. Format: latitude,longitude
    WEIGHT Module path to weight function, eg. "routor.weights.length"
    """
    set_log_level(log_level)

    # load weight function
    from importlib import import_module

    module_path, func_name = weight.rsplit('.', 1)
    module = import_module(module_path)
    weight_func = getattr(module, func_name)

    # do routing
    data = engine.route(map_path, origin, destination, weight_func)

    print(json.dumps(data.dict(), indent=2))
