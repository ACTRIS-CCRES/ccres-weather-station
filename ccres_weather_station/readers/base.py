from abc import ABC, abstractmethod

import xarray as xr

from ccres_weather_station.types import PathLike, PathsLike


class BaseReader(ABC):
    """BaseReader Base reader to implement for registering readers."""

    @abstractmethod
    def read_file(self, file: PathLike) -> xr.Dataset:
        pass

    @abstractmethod
    def read_files(self, files: PathsLike) -> xr.Dataset:
        pass
