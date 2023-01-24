"""Module that handle some attributes generation.

Also handle saving of file.
"""

import datetime as dt
from pathlib import Path

import pandas as pd
import xarray as xr


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
    """_get_software_git_infos Get a formatted string with software infos.

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
    """add_created_date Add created_date field into the dataset.

    Add the datetime.now() string representation
    """
    ds.attrs["created_date"] = str(dt.datetime.utcnow())
    return ds


def add_date_metadata_modified(ds: xr.Dataset) -> xr.Dataset:
    """add_created_date Add metadata_modified field into the dataset.

    Add the datetime.now() string representation
    """
    ds.attrs["metadata_modified"] = str(dt.datetime.utcnow())
    return ds
