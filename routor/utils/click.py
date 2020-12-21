import click

from .. import models


class LocationParamType(click.ParamType):
    name = "LATITUDE,LONGITUDE"

    def convert(self, value: str, param, ctx) -> models.Location:
        """
        Parse comma separated GPS coordinates.
        """
        try:
            latitude_str, longitude_str = value.split(',')
        except ValueError:
            self.fail("expected two items separated by comma", param, ctx)

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except ValueError:
            self.fail("Invalid number", param, ctx)

        return models.Location(latitude=latitude, longitude=longitude)
