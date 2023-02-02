from abc import ABC, abstractmethod

import xarray as xr

from ccres_weather_station.config.config import Config
from ccres_weather_station.types import PathLike, PathsLike


class BaseReader(ABC):
    """Base reader to implement for registering readers."""

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def read_file(self, file: PathLike) -> xr.Dataset:
        pass

    @abstractmethod
    def read_files(self, files: PathsLike) -> xr.Dataset:
        pass
