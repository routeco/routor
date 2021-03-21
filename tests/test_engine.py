from routor import models, weights
from routor.engine import Engine

ORIGIN_LOCATION = models.Location(latitude=51.4996612, longitude=-2.6823825)
ORIGN_NODE_ID = 1468922197
DESTINATION_LOCATION = models.Location(latitude=51.4973375, longitude=-2.682841)
DESTINATION_NODE_ID = 305907

PATH = [
    1468922197,
    2106393640,
    1468922198,
    331786,
    1591662562,
    2106389513,
    21029782,
    21029787,
    2106389521,
    1591662563,
    2106389517,
    2106389524,
    1591662567,
    2106389522,
    21029783,
    2106389519,
    331775,
    2106389530,
    1591662579,
    2106389531,
    21029784,
    2106389515,
    2106389532,
    1591662581,
    2106389523,
    2106389533,
    21029785,
    2106389534,
    2106389528,
    1591662585,
    2106389525,
    2106389527,
    1591662587,
    2106389512,
    2106389518,
    21029786,
    2106389514,
    1591662583,
    2106389529,
    2106389520,
    2106393654,
    305903,
    305905,
    2983641842,
    305907,
]


def test_get_closest_node(engine: Engine) -> None:
    """
    Identify closest node.
    """
    node = engine.get_closest_node(ORIGIN_LOCATION)
    assert node.node_id == ORIGN_NODE_ID


def test_find_path(engine: Engine) -> None:
    """
    Make sure we calculate a proper path.
    """
    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)

    path = engine.find_path(origin, destination, weights.travel_time)
    node_ids = [node.node_id for node in path]
    assert node_ids == PATH


def test_route__weight_func(mocker, engine: Engine) -> None:
    """
    Make sure the weight function is used.
    """
    mocker.spy(weights, "length")
    mocker.spy(weights, "travel_time")
    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)

    engine.route(origin, destination, weights.length, weights.travel_time)
    edge_count = len(PATH) - 1
    assert weights.length.call_count > len(PATH)  # type: ignore
    assert weights.travel_time.call_count == edge_count  # type: ignore


def test_costs_for_path(engine: Engine) -> None:
    """
    Make sure costs are summed up correctly.
    """
    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)
    path = engine.find_path(origin, destination, weights.travel_time)

    costs = engine.costs_for_path(path, weights.travel_time)
    assert costs == 46.199999999999996


def test_length_of_path(engine: Engine) -> None:
    """
    Make sure the length is derived correctly.
    """
    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)
    path = engine.find_path(origin, destination, weights.travel_time)

    length = engine.length_of_path(path)
    assert length == 1449.668  # meters


def test_travel_time_of_path(engine: Engine) -> None:
    """
    Make sure the travel time is derived correctly.
    """
    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)
    path = engine.find_path(origin, destination, weights.travel_time)

    length = engine.travel_time_of_path(path, weights.travel_time)
    assert length == 46.199999999999996  # seconds


def test_travel_time_of_path__custom_func(engine: Engine) -> None:
    """
    Make sure the travel time is derived correctly.
    """

    def my_travel_time(*args, **kwargs) -> float:
        return 1

    origin = engine.get_closest_node(ORIGIN_LOCATION)
    destination = engine.get_closest_node(DESTINATION_LOCATION)
    path = engine.find_path(origin, destination, weights.travel_time)

    length = engine.travel_time_of_path(path, my_travel_time)
    edge_count = len(PATH) - 1
    assert length == edge_count  # each edge has a travel_time of 1
