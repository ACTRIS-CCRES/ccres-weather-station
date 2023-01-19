""" Module that handle some attributes generation and also the saving of file
"""

import pandas as pd
from pathlib import Path
import datetime as dt


def add_time_coverage_attributes(ds, dim_time):
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

    if len(time) > 0:
        time_coverage_start = time[0].isoformat()
        time_coverage_end = time[-1].isoformat()
        time_coverage_duration = (time[-1] - time[0]).isoformat()

    if len(time) > 1:
        time_coverage_resolution = (time[1] - time[0]).isoformat()

    ds.attrs["time_coverage_start"] = time_coverage_start
    ds.attrs["time_coverage_end"] = time_coverage_end
    ds.attrs["time_coverage_duration"] = time_coverage_duration
    ds.attrs["time_coverage_resolution"] = time_coverage_resolution
    return ds


def _get_software_git_infos():
    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError:
        return ""

    try:
        main_repo = Repo(
            str(Path(__file__).parent), search_parent_directories=True
        )

        hash_last_commit_message = main_repo.head.commit.hexsha

        tag_version = "None"
        tags = main_repo.tags
        if tags != []:
            tag_version = tags[-1]

        return (
            f"TAG = {tag_version}, COMMIT_HASH = {hash_last_commit_message}."
        )

    except InvalidGitRepositoryError:
        return ""


def add_history(ds):
    history = f"Created on {pd.Timestamp.now().isoformat()}.{_get_software_git_infos()}"
    ds.attrs["history"] = history
    return ds


def add_created_date(ds):
    # Add production as execution script date.
    ds.attrs["created_date"] = str(dt.datetime.utcnow())
    return ds


def add_date_metadata_modified(ds):
    # Add production as execution script date.
    ds.attrs["metadata_modified"] = str(dt.datetime.utcnow())
    return ds
