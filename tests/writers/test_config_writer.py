import pandas as pd
import pytest
import xarray as xr

from ccres_weather_station.config.config import (
    Config,
    CoordConfig,
    CoordEncoding,
    CoordMeta,
    VariableConfig,
    VariableEncoding,
    VariableMeta,
)
from ccres_weather_station.writers.write import ConfigWriter


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


@pytest.fixture()
def config():
    config = Config(
        variables={
            "var": VariableConfig(
                "var",
                meta=VariableMeta(standard_name="var", long_name="Variable long name"),
                encoding=VariableEncoding(dtype="float32"),
            )
        },
        coords={
            "time": CoordConfig(
                "time",
                meta=CoordMeta(standard_name="time", long_name="Date"),
                encoding=CoordEncoding(
                    units="seconds since 1970-01-01", calendar="standard"
                ),
            )
        },
        attrs={"standard_name_vocabulary": "CF Standard Name Table v79"},
    )

    return config


@pytest.fixture()
def empty_config():
    config = Config(
        variables={},
        coords={},
        attrs={},
    )

    return config


@pytest.fixture()
def complex_config():
    config = Config(
        variables={
            "unexisting_var": VariableConfig(
                "unexisting_var",
                meta=VariableMeta(
                    standard_name="unexisting_var",
                    long_name="Unexisting variable long name",
                ),
                encoding=VariableEncoding(),
            ),
            "var": VariableConfig(
                "var",
                meta=VariableMeta(
                    standard_name="var", long_name="New variable long name"
                ),
                encoding=VariableEncoding(dtype="float32"),
            ),
        },
        coords={
            "unexisting_time": CoordConfig(
                "unexisting_time",
                meta=CoordMeta(standard_name="unexisting_time", long_name="Date"),
                encoding=CoordEncoding(
                    units="seconds since 1970-01-01", calendar="standard"
                ),
            ),
            "time": CoordConfig(
                "time",
                meta=CoordMeta(standard_name="time", long_name="New Date"),
                encoding=CoordEncoding(
                    units="seconds since 1970-01-01", calendar="standard"
                ),
            ),
        },
        attrs={"standard_name_vocabulary": "New CF attribute"},
    )

    return config


def test_add_config_meta(ds, config):
    assert "long_name" not in ds["var"].attrs
    assert "long_name" not in ds["time"].attrs
    assert "standard_name_vocabulary" not in ds.attrs
    config_writer = ConfigWriter(config)
    ds = config_writer.add_config_meta(ds)
    assert "long_name" in ds["var"].attrs
    assert ds["var"].attrs["long_name"] == "Variable long name"
    assert "long_name" in ds["time"].attrs
    assert ds["time"].attrs["long_name"] == "Date"
    assert "standard_name_vocabulary" in ds.attrs
    assert ds.attrs["standard_name_vocabulary"] == "CF Standard Name Table v79"


def test_add_config_meta_empty_config(ds, empty_config):
    assert "long_name" not in ds["var"].attrs
    config_writer = ConfigWriter(empty_config)
    ds = config_writer.add_config_meta(ds)
    assert "long_name" not in ds["var"].attrs


def test_add_config_meta_complex(ds, config, complex_config):
    assert "long_name" not in ds["var"].attrs
    assert "long_name" not in ds["time"].attrs
    assert "standard_name_vocabulary" not in ds.attrs
    config_writer = ConfigWriter(config)
    complex_config_writer = ConfigWriter(complex_config)
    ds = config_writer.add_config_meta(ds)
    assert "long_name" in ds["var"].attrs
    assert ds["var"].attrs["long_name"] == "Variable long name"
    assert "long_name" in ds["time"].attrs
    assert ds["time"].attrs["long_name"] == "Date"
    assert "standard_name_vocabulary" in ds.attrs
    assert ds.attrs["standard_name_vocabulary"] == "CF Standard Name Table v79"

    ds = complex_config_writer.add_config_meta(ds)
    assert "long_name" in ds["var"].attrs
    assert ds["var"].attrs["long_name"] == "New variable long name"
    assert "long_name" in ds["time"].attrs
    assert ds["time"].attrs["long_name"] == "New Date"
    assert "standard_name_vocabulary" in ds.attrs
    assert ds.attrs["standard_name_vocabulary"] == "New CF attribute"


def test_get_encoding(ds, config):
    config_writer = ConfigWriter(config)
    encoding = config_writer.get_encoding(ds)
    assert "time" in encoding
    assert "units" in encoding["time"]
    assert encoding["time"]["units"] == "seconds since 1970-01-01"
    assert "var" in encoding
    assert "dtype" in encoding["var"]
    assert encoding["var"]["dtype"] == "float32"


def test_get_encoding_empty_config(ds, empty_config):
    config_writer = ConfigWriter(empty_config)
    encoding = config_writer.get_encoding(ds)
    assert encoding == {}


def test_get_encoding_complex(ds, complex_config):
    config_writer = ConfigWriter(complex_config)
    encoding = config_writer.get_encoding(ds)
    assert "unexisting_time" not in encoding
    assert "unexisting_var" not in encoding
    assert "time" in encoding
    assert "units" in encoding["time"]
    assert encoding["time"]["units"] == "seconds since 1970-01-01"
    assert "var" in encoding
    assert "dtype" in encoding["var"]
    assert encoding["var"]["dtype"] == "float32"
