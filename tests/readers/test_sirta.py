import os

import pandas as pd
import xarray as xr
from pathlib import Path
from ccres_weather_station.readers.sirta import SirtaReader
from ccres_weather_station.config.config import Config

SIRTA_FILE = Path(
    Path(__file__).parent
    / "../data/sirta/meteoairsol_1a_Lz1NairF1minPtuvPrain_v01_20201010_000000_1440.asc"
)


def test_sirta_reader():
    config = Config.default()
    ds = SirtaReader(config=config).read(SIRTA_FILE)
    time = ds.coords[config.coords["time"].name]

    assert isinstance(ds, xr.Dataset)
    assert len(time) == 1440
    assert time[0] == pd.Timestamp(2020, 10, 10, 0, 0, 0)
    assert time[-1] == pd.Timestamp(2020, 10, 10, 23, 59, 0)
    assert config.coords["time"].name in ds.coords
