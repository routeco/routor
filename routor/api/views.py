from importlib.metadata import version  # type: ignore
from typing import List

from fastapi import FastAPI

from .. import engine
from .. import models as engine_models
from .. import weights
from . import models
from .settings import settings

app = FastAPI()


@app.get("/version", response_model=models.VersionResponse)
def read_version() -> models.VersionResponse:
    """
    Return the package version of routor.
    """
    return models.VersionResponse(version=version("routor"))


@app.get("/weights", response_model=List[str])
def read_weights() -> List[str]:
    """
    Return all possible weight functions.
    """
    return weights.get_function_names()


@app.get("/route", response_model=engine_models.Route)
def read_route(
    data: models.RouteRequest,
) -> engine_models.Route:
    """
    Calculate a route from A to B.
    """
    route = engine.route(settings.map_path, data.origin, data.destination, data.weight)
    return route
