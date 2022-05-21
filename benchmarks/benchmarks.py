from pathlib import Path

from routor import weights
from routor.engine import Engine
from routor.models import Location
from routor.utils import graph as graph_utils

MAP_PATH = Path(".").absolute() / "benchmark_map.graphml"


class TimeSuite:
    def setup_cache(self):
        graph = graph_utils.download_map(
            ["bristol"],
            node_tags=["osmid"],
            edge_tags=["junction", "traffic_signals", "surface", "lanes"],
            api_key=None,
        )
        graph_utils.save_map(graph, MAP_PATH)

    def setup(self):
        self.engine = Engine(MAP_PATH)

    def time_load_map(self):
        Engine(MAP_PATH)

    def time_routing(self):
        origin = Location(longitude=-2.583160400390625, latitude=51.43806566801884)
        destination = Location(
            longitude=-2.6348304748535156, latitude=51.48223813101211
        )
        self.engine.route(origin, destination, weights.length, weights.travel_time)


if __name__ == "__main__":
    suite = TimeSuite()
    suite.setup_cache()
    suite.setup()

    suite.time_routing()
