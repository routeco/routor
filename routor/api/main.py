from typing import List

from fastapi import Depends, FastAPI

from .. import engine
from .. import models as engine_models
from .. import weights
from . import models
from .config import settings

app = FastAPI()


class PersistentEngine(engine.Engine):
    def __init__(self):
        super().__init__(settings.map_path)


@app.get("/weights", response_model=List[str])
def read_weights() -> List[str]:
    """
    Return all possible weight functions.
    """
    return weights.get_function_names()


@app.get("/route", response_model=engine_models.Route)
def read_route(
    data: models.RouteRequest,
    engine: PersistentEngine = Depends(),  # noqa: B008
) -> engine_models.Route:
    """
    Calculate a route from A to B.
    """
    weight_func = weights.get_function(data.weight)

    route = engine.route(data.origin, data.destination, weight_func)
    return route
