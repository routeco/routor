import logging
from functools import lru_cache
from typing import List

from fastapi import Depends, FastAPI

from .. import engine
from .. import models as engine_models
from .. import weights
from . import config, models

logger = logging.getLogger()
app = FastAPI()


@lru_cache()
def get_settings() -> config.Settings:
    """
    Return application settings.
    """
    logger.debug("initialise settings")
    return config.Settings()


def get_engine(
    settings: config.Settings = Depends(get_settings),  # noqa: B008
) -> engine.Engine:
    """
    Return an initialised routing engine.

    This is a singletone and the engine is only initialised once.
    """
    cached_value = getattr(get_engine, "__cache", None)
    if not cached_value:
        logger.debug("initialise engine")
        cached_value = engine.Engine(settings.map_path)
        get_engine.__cache = cached_value  # type: ignore
    return cached_value


@app.get("/weights", response_model=List[str])
def read_weights() -> List[str]:
    """
    Return all possible weight functions.
    """
    return weights.get_function_names()


@app.get("/route", response_model=engine_models.Route)
def read_route(
    data: models.RouteRequest,
    engine: engine.Engine = Depends(get_engine),  # noqa: B008
    settings: config.Settings = Depends(get_settings),  # noqa: B008
) -> engine_models.Route:
    """
    Calculate a route from A to B.
    """
    weight_func = weights.get_function(data.weight)

    route = engine.route(
        data.origin, data.destination, weight_func, settings.get_travel_time_func()
    )
    return route
