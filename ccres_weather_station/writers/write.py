"""Module that handle some attributes generation.

Also handle saving of file.
"""

import datetime as dt
from pathlib import Path
from typing import Dict

import pandas as pd
import xarray as xr

from ccres_weather_station.config.config import Config
from ccres_weather_station.types import PathLike


def add_time_coverage_attributes(ds: xr.Dataset, dim_time: str) -> xr.Dataset:
    time = pd.to_datetime(ds[dim_time].values)

    if isinstance(time, pd.Timestamp):
        # Convert do nothing if already that, but if only
        # one time value, then pandas return a timestamp object
        #  need to reconvert it
        time = pd.DatetimeIndex([time])

    time_coverage_start = ""
    time_coverage_end = ""
    time_coverage_duration = ""
    time_coverage_resolution = ""

    if time.size > 0:
        time_coverage_start = time[0].isoformat()
        time_coverage_end = time[-1].isoformat()
        time_coverage_duration = (time[-1] - time[0]).isoformat()

    if time.size > 1:
        time_coverage_resolution = (time[1] - time[0]).isoformat()

    ds.attrs["time_coverage_start"] = time_coverage_start
    ds.attrs["time_coverage_end"] = time_coverage_end
    ds.attrs["time_coverage_duration"] = time_coverage_duration
    ds.attrs["time_coverage_resolution"] = time_coverage_resolution
    return ds


def _get_software_git_infos() -> str:
    """Get a formatted string with software infos.

    Returns
    -------
    str
        formatted string with software infos
    """
    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError:
        return ""

    try:
        main_repo = Repo(str(Path(__file__).parent), search_parent_directories=True)

        hash_last_commit_message = main_repo.head.commit.hexsha

        tag_version = "None"
        tags = main_repo.tags
        if tags != []:
            tag_version = tags[-1]

        return f"TAG = {tag_version}, COMMIT_HASH = {hash_last_commit_message}."

    except InvalidGitRepositoryError:
        return ""


def add_history(ds: xr.Dataset) -> xr.Dataset:
    history = f"Created on {pd.Timestamp.now().isoformat()}.{_get_software_git_infos()}"
    ds.attrs["history"] = history
    return ds


def add_created_date(ds: xr.Dataset) -> xr.Dataset:
    """Add created_date field into the dataset.

    Add the datetime.now() string representation
    """
    ds.attrs["created_date"] = str(dt.datetime.utcnow())
    return ds


def add_date_metadata_modified(ds: xr.Dataset) -> xr.Dataset:
    """Add metadata_modified field into the dataset.

    Add the datetime.now() string representation
    """
    ds.attrs["metadata_modified"] = str(dt.datetime.utcnow())
    return ds


class ConfigWriter:
    def __init__(self, config: Config):
        self.config = config

    def _add_var_attrs(self, ds: xr.Dataset) -> xr.Dataset:
        for _, conf_var in self.config.variables.items():
            if conf_var.name not in ds.data_vars:
                continue
            for attr, value in conf_var.meta:
                if value is None:
                    continue
                ds[conf_var.name].attrs[attr] = value
        return ds

    def _add_coord_attrs(self, ds: xr.Dataset) -> xr.Dataset:
        for _, conf_coord in self.config.coords.items():
            if conf_coord.name not in ds.coords:
                continue
            for attr, value in conf_coord.meta:
                if value is None:
                    continue
                ds[conf_coord.name].attrs[attr] = value
        return ds

    def _add_global_attrs(self, ds: xr.Dataset) -> xr.Dataset:
        for attr, value in self.config.attrs.items():
            if value is not None:
                ds.attrs[attr] = value
        return ds

    def add_config_meta(self, ds: xr.Dataset) -> xr.Dataset:
        """Add the metadata to the xarray dataset.

        Add :
        - Variables metadata
        - Coordinates metadata
        - Global attributes

        Parameters
        ----------
        ds : xr.Dataset
            xarray dataset

        Returns
        -------
        xr.Dataset
            The dataset with metadata added
        """
        ds = self._add_var_attrs(ds)
        ds = self._add_coord_attrs(ds)
        ds = self._add_global_attrs(ds)
        return ds

    def _get_var_encoding(
        self,
        ds: xr.Dataset,
        encoding: Dict[str, Dict[str, str]],
    ) -> Dict[str, Dict[str, str]]:
        """Get the variables encoding from config file."""
        for _, encoding_var in self.config.variables.items():
            if encoding_var.name not in ds.data_vars:
                continue
            encoding[encoding_var.name] = {}
            for key, value in encoding_var.encoding:
                if value is None:
                    continue
                encoding[encoding_var.name][key] = value
        return encoding

    def _get_coord_encoding(
        self,
        ds: xr.Dataset,
        encoding: Dict[str, Dict[str, str]],
    ) -> Dict[str, Dict[str, str]]:
        """Get the coordinates encoding from config file."""
        for _, encoding_coord in self.config.coords.items():
            if encoding_coord.name not in ds.coords:
                continue
            encoding[encoding_coord.name] = {}
            for key, value in encoding_coord.encoding:
                if value is None:
                    continue
                encoding[encoding_coord.name][key] = value
        return encoding

    def get_encoding(self, ds: xr.Dataset) -> Dict[str, Dict[str, str]]:
        """Parse the config file to extract the encoding for netcdf.

        Parse both coordinates and variables

        Parameters
        ----------
        ds : xr.Dataset
            xarray dataset

        Returns
        -------
        Dict[str, Dict[str, str]]
            Dictionnary of encoding terms
        """
        encoding: Dict[str, Dict[str, str]] = {}
        encoding = self._get_var_encoding(ds, encoding)
        encoding = self._get_coord_encoding(ds, encoding)
        return encoding


def write_nc(ds: xr.Dataset, config: Config, output_path: PathLike) -> None:
    output_path = Path(output_path)
    config_writer = ConfigWriter(config)
    ds = add_time_coverage_attributes(ds, config.coords["time"].name)
    ds = add_history(ds)
    ds = add_created_date(ds)
    ds = add_date_metadata_modified(ds)
    ds = config_writer.add_config_meta(ds)
    encoding = config_writer.get_encoding(ds)
    ds.to_netcdf(output_path, encoding=encoding)
