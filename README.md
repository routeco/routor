# routor

![PyPI](https://img.shields.io/pypi/v/routor?style=flat-square)
![GitHub Workflow Status (main)](https://img.shields.io/github/workflow/status/escaped/routor/Test%20&%20Lint/main?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/routor/main?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/routor?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/routor?style=flat-square)

Simple osm routing engine.

## Requirements

* Python 3.6.1 or newer

## Installation

```sh
pip install routor
```

## Usage

### CLI

The CLI offers multiple commands, use `routor --help` to find out more.

#### Download map

Downloads a compatible map from OSM, eg.

```sh
routor download "Bristol, England" ./bristol.graphml
```

#### Calculate route

Determine the optimal route between two points using the given weight function and print the route as `JSON` to `stdout`.

```sh
routor route -- ./bristol.graphml  "51.47967237816338,-2.6174926757812496" "51.45422084861252,-2.564105987548828" "routor.weights.length"
```

### Web API

#### Configuration

The configuration is either read from a `.env` file or the environment.
Before you are able to run the server, you have to set the variables mentioned in [routor/api/config.py](routor/api/config.py).

#### Run the API

The api is served using [uvicorn](https://www.uvicorn.org/).
To start the server run

```sh
uvicorn routor.api:app
```

The API will be available at http://127.0.0.1:8000 and the docs at http://127.0.0.1:8000/docs.

#### Register a new weight function

Existing weight functions are defined in [routor/weights.py](routor/weights.py).
To add a new weight functon, you have to create a new project and add `routor` as dependency.
Create a new file, eg. `main.py` and add the following content, which will become the entrypoint for `uvicorn`.

```python
# main.py
from typing import Optional

from routor.api.main import app  # noqa
from routor.weights import register
from routor import models


def my_weight_func(prev_edge: Optional[models.Edge], edge: models.Edge) -> float:
    ...
    return ...


register(my_weight_func, "weight_func")
```

Start the server with `uvicorn main:app` and the weight function will be available as `weight_func` when calling the api.

### As library

You can also use the engine as a library.
To calculate a route from A to B you can do

```python
from routor.engine import Engine
from routor import models, weights

...
map_path = Path(...)
engine = Engine(map_path)

origin = models.Location(latitude=51.47967237816338, longitude=-2.6174926757812496)
destination = models.Location(latitude=51.45422084861252, longitude=-2.564105987548828)

route = engine.route(origin, destination, weights.length)  # shortest distance
```

## Available weight-functions

### `"length"` / `routor.weights.length`

Calculates the shortest path from A to B, only the length of an edge is taken into account.

### `"travel_time"` / `routor.weight.travel_time`

Calculates the fastest route based on [travel time](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.speed.add_edge_travel_times).

## Development

This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

Additionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) are installed to provide a better debugging experience.
To enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.

Clone this repository and run

```bash
poetry install
poetry run pre-commit install
```

to create a virtual enviroment containing all dependencies.
Afterwards, You can run the test suite using

```bash
poetry run pytest
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.

### Cookiecutter template

This project was created using [cruft](https://github.com/cruft/cruft) and the
[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.
In order to update this repository to the latest template version run

```sh
cruft update
```

in the root of this repository.
