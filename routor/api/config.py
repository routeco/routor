from pathlib import Path

from pydantic import BaseSettings, validator

from routor.utils import core as core_utils
from routor.weights import WeightFunction


class Settings(BaseSettings):
    map_path: Path
    travel_time_func: str = "routor.weights.travel_time"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @validator('travel_time_func')
    def _validate_travel_time_func(cls, func_path):  # noqa: N805
        """
        Make sure that the travel_function is importable
        """
        core_utils.import_weight_function(func_path)
        return func_path

    def get_travel_time_func(self) -> WeightFunction:
        """
        Get the configured travel time function.
        """
        return core_utils.import_weight_function(self.travel_time_func)
