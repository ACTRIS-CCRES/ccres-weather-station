from abc import ABC, abstractmethod

import xarray as xr

from ccres_weather_station.types import PathLike


class BaseReader(ABC):
    """BaseReader Base reader to implement for registering readers."""

    @abstractmethod
    def read(self, file: PathLike) -> xr.Dataset:
        pass
