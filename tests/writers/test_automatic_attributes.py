import datetime as dt

import pandas as pd
import pytest
import xarray as xr

from ccres_weather_station.writers.write import (
    add_created_date,
    add_date_metadata_modified,
    add_history,
    add_time_coverage_attributes,
)


@pytest.fixture()
def ds():
    time = pd.date_range("2010-01-01", "2010-01-02", freq="1H")
    var = [0] * len(time)
    ds = xr.Dataset(
        {
            "var": (["time"], var),
        },
        coords={
            "time": time,
        },
    )
    return ds


def test_add_time_coverage_attributes(ds):
    ds = add_time_coverage_attributes(ds, "time")
    assert "time_coverage_start" in ds.attrs
    assert "time_coverage_end" in ds.attrs
    assert "time_coverage_duration" in ds.attrs
    assert "time_coverage_resolution" in ds.attrs
    assert ds.attrs["time_coverage_start"] == "2010-01-01T00:00:00"
    assert ds.attrs["time_coverage_end"] == "2010-01-02T00:00:00"
    assert ds.attrs["time_coverage_duration"] == "P1DT0H0M0S"
    assert ds.attrs["time_coverage_resolution"] == "P0DT1H0M0S"


def test_add_time_coverage_attributes_one_time(ds):
    ds = ds.sel({"time": ds["time"][0]})
    ds = add_time_coverage_attributes(ds, "time")
    assert "time_coverage_start" in ds.attrs
    assert "time_coverage_end" in ds.attrs
    assert "time_coverage_duration" in ds.attrs
    assert "time_coverage_resolution" in ds.attrs
    assert ds.attrs["time_coverage_start"] == "2010-01-01T00:00:00"
    assert ds.attrs["time_coverage_end"] == "2010-01-01T00:00:00"
    assert ds.attrs["time_coverage_duration"] == "P0DT0H0M0S"
    assert ds.attrs["time_coverage_resolution"] == ""


def test_add_time_coverage_attributes_two_time(ds):
    ds = ds.sel({"time": ds["time"][0:2]})
    ds = add_time_coverage_attributes(ds, "time")
    assert "time_coverage_start" in ds.attrs
    assert "time_coverage_end" in ds.attrs
    assert "time_coverage_duration" in ds.attrs
    assert "time_coverage_resolution" in ds.attrs
    assert ds.attrs["time_coverage_start"] == "2010-01-01T00:00:00"
    assert ds.attrs["time_coverage_end"] == "2010-01-01T01:00:00"
    assert ds.attrs["time_coverage_duration"] == "P0DT1H0M0S"
    assert ds.attrs["time_coverage_resolution"] == "P0DT1H0M0S"


def test_add_time_coverage_attributes_zero_time(ds):
    ds = ds.sel({"time": []})
    ds = add_time_coverage_attributes(ds, "time")
    assert "time_coverage_start" in ds.attrs
    assert "time_coverage_end" in ds.attrs
    assert "time_coverage_duration" in ds.attrs
    assert "time_coverage_resolution" in ds.attrs
    assert ds.attrs["time_coverage_start"] == ""
    assert ds.attrs["time_coverage_end"] == ""
    assert ds.attrs["time_coverage_duration"] == ""
    assert ds.attrs["time_coverage_resolution"] == ""


def test_add_history(ds):
    ds = add_history(ds)
    assert "history" in ds.attrs
    assert "COMMIT_HASH" in ds.attrs["history"]
    assert "TAG" in ds.attrs["history"]


def test_add_created_date(ds):
    ds = add_created_date(ds)
    assert "created_date" in ds.attrs
    created_date = pd.to_datetime(ds.attrs["created_date"])
    assert created_date <= pd.to_datetime(dt.datetime.utcnow())


def test_add_date_metadata_modified(ds):
    ds = add_date_metadata_modified(ds)
    assert "metadata_modified" in ds.attrs
    metadata_modified = pd.to_datetime(ds.attrs["metadata_modified"])
    assert metadata_modified <= pd.to_datetime(dt.datetime.utcnow())
