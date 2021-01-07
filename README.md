# routor

![PyPI](https://img.shields.io/pypi/v/routor?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/escaped/routor/Test%20&%20Lint/master?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/routor/master?style=flat-square)
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

Use the integrated cli to calculate a route.

```text
$ python -m routor --help
Usage: python -m routor [OPTIONS] MAP ORIGIN DESTINATION [travel_time|length]

  Calculate a shortest path.

  MAP Path to an OSM file. Format: .osm.xml
  ORIGIN GPS location. Format: latitude,longitude
  DESTINATION GPS location. Format: latitude,longitude

Options:
  --help  Show this message and exit.
```

## Development

This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

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
