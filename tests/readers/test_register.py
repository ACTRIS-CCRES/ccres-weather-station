import pytest
import xarray as xr

from ccres_weather_station.readers.base import BaseReader
from ccres_weather_station.readers.register import READERS, register_reader
from ccres_weather_station.types import PathLike


def test_register_good_reader():
    class GoodReader(BaseReader):
        def read(self, file: PathLike) -> xr.Dataset:
            return xr.Dataset()

    assert "good_reader" not in READERS
    register_reader(GoodReader, "good_reader")
    assert "good_reader" in READERS


def test_register_no_implementation():
    class BadReader(BaseReader):
        pass

    with pytest.raises(TypeError):
        register_reader(BadReader, "bad_reader")


def test_register_bad_reader():
    class BadReader:
        pass

    with pytest.raises(TypeError):
        register_reader(BadReader, "bad_reader")
