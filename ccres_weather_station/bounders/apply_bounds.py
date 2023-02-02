import datetime as dt
from typing import Optional

import xarray as xr

from ccres_weather_station.config.config import Config


def apply_bounds(
    ds: xr.Dataset,
    config: Config,
    start_date: Optional[dt.datetime],
    end_date: Optional[dt.datetime],
) -> xr.Dataset:
    """Apply boundaries cut to the dataset.

    Cut the from start_date to end_date.

    Parameters
    ----------
    ds : xr.Dataset
        Incoming xarray dataset
    config : Config
        Configuration object
    start_date : Optional[dt.datetime]
        Date from which to keep all output data
    end_date : Optional[dt.datetime]
        Date from which to remove all output data

    Returns
    -------
    xr.Dataset
        Cutted xarray dataset
    """
    return ds.sel({config.coords["time"].name: slice(start_date, end_date)})
