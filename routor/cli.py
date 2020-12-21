import json
from pathlib import Path

import click

from . import models, weights
from .engine import route
from .utils.click import LocationParamType


@click.command()
@click.argument('map', type=click.Path(exists=True, dir_okay=False))
@click.argument('origin', type=LocationParamType())
@click.argument('destination', type=LocationParamType())
@click.argument('weight', type=click.Choice(weights.get_function_names()))
def main(
    map: Path, origin: models.Location, destination: models.Location, weight: str
) -> None:
    """
    Calculate a shortest path.

    \b
    MAP Path to an OSM file. Format: .osm.xml
    ORIGIN GPS location. Format: latitude,longitude
    DESTINATION GPS location. Format: latitude,longitude
    """
    data = route(map, origin, destination, weight)

    print(json.dumps(data.dict(), indent=2))
