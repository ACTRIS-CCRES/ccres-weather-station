from pathlib import Path

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
from ccres_weather_station.writers.write import write_nc


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


def test_write(ds, config, tmp_path: Path):
    directory = tmp_path / "output"
    directory.mkdir()
    output_file = directory / "test.nc"
    assert not output_file.exists()
    write_nc(ds, config, output_file)
    assert output_file.exists()
