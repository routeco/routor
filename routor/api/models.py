from pydantic import BaseModel, validator

from .. import models, weights


class VersionResponse(BaseModel):
    version: str


class RouteRequest(BaseModel):
    origin: models.Location
    destination: models.Location
    weight: str

    @validator("weight")
    def validate_weight(cls, value: str) -> str:  # noqa: N805
        valid_values = weights.get_function_names()
        if value not in valid_values:
            raise ValueError(
                f"Invalid weight function. Possible values are: {valid_values}"
            )
        return value
