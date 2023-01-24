from pathlib import Path
from typing import Any, Union

import numpy as np
import pandas as pd
import xarray as xr

from ccres_weather_station.config.config import Config
from ccres_weather_station.readers.base import BaseReader
from ccres_weather_station.readers.register import register_reader


def _sirta_date_parser(concatenated_column: Any) -> Any:
    """_sirta_date_parser pandas will pass.

    1) Pass one or more arrays (as defined by parse_dates) as arguments
    2) concatenate (row-wise) the string values from the columns defined by
        parse_dates into a single array and pass that
    3) call date_parser once for each row using one or more strings
        (corresponding to the columns defined by parse_dates) as arguments.

    By having only one function argument we fall in case 1) if only one column
    or case 2 otherwise.

    Returns
    -------
    Any
        Types described here :
        https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    """
    return pd.to_datetime(concatenated_column, format="%Y-%m-%dT%H:%M:%SZ")


class SirtaReader(BaseReader):
    def __init__(self, config: Config):
        self.config = config

    def read(self, path: Union[str, Path]) -> xr.Dataset:
        path = Path(path)
        columns_map = {
            self.config.coords["time"].name: 0,
            self.config.variables["wind_speed"].name: 1,
            self.config.variables["wind_direction"].name: 2,
            self.config.variables["air_temperature"].name: 3,
            self.config.variables["relative_humidity"].name: 4,
            self.config.variables["pressure"].name: 5,
            self.config.variables["precipitation_rate"].name: 6,
        }
        columns_type = {
            self.config.coords["time"].name: str,
            self.config.variables["wind_speed"].name: np.float32,
            self.config.variables["wind_direction"].name: np.float32,
            self.config.variables["air_temperature"].name: np.float32,
            self.config.variables["relative_humidity"].name: np.float32,
            self.config.variables["pressure"].name: np.float32,
            self.config.variables["precipitation_rate"].name: np.float32,
        }

        names = list(columns_map.keys())
        number_positions = list(columns_map.values())
        df = pd.read_csv(
            str(path.resolve()),
            names=names,
            usecols=number_positions,
            dtype=columns_type,
            comment="#",
            parse_dates=[0],
            date_parser=_sirta_date_parser,
            delim_whitespace=True,
            encoding="utf-8",
        )
        df = df.set_index(self.config.coords["time"].name)
        return df.to_xarray()


register_reader(SirtaReader, "sirta")
