from pathlib import Path

import pytest

from ccres_weather_station.config.config import Config

DEFAULT_CONFIG_FILE = Path(
    Path(__file__).parent.parent / "data/config_files/default.toml"
)
CUSTOM_CONFIG_FILE = Path(
    Path(__file__).parent.parent / "data/config_files/custom.toml"
)
NO_ATTRS = Path(Path(__file__).parent.parent / "data/config_files/no_attrs.toml")

NO_VARS = Path(Path(__file__).parent.parent / "data/config_files/no_vars.toml")
NO_COORDS = Path(Path(__file__).parent.parent / "data/config_files/no_coords.toml")

NO_VAR_NAME = Path(Path(__file__).parent.parent / "data/config_files/no_var_name.toml")
NO_COORD_NAME = Path(
    Path(__file__).parent.parent / "data/config_files/no_coord_name.toml"
)


def test_good_config():
    config = Config.from_toml(DEFAULT_CONFIG_FILE)
    assert isinstance(config, Config)
    assert "wind_direction" in config.variables
    assert "time" in config.coords
    assert len(config.attrs) > 0


def test_good_config_var_iterables():
    config = Config.from_toml(DEFAULT_CONFIG_FILE)
    d_meta = dict(config.variables["wind_direction"].meta)
    d_encoding = dict(config.coords["time"].encoding)
    assert isinstance(d_meta, dict)
    assert isinstance(d_encoding, dict)


def test_good_config_add_custom_config():
    config = Config.from_toml(DEFAULT_CONFIG_FILE)
    assert config.variables["wind_speed"].meta.long_name == "Wind speed"
    assert "custom_var" not in config.variables
    assert config.variables["wind_speed"].meta.units == "m.s^-1"

    config.add_config_from_toml(CUSTOM_CONFIG_FILE)
    assert (
        config.variables["wind_speed"].meta.long_name
        == "My custom wind speed long name"
    )
    assert "custom_var" in config.variables
    # Test if None is not set
    assert config.variables["wind_speed"].meta.units == "m.s^-1"


def test_add_no_global_attrs():
    config = Config.from_toml(DEFAULT_CONFIG_FILE)
    config.add_config_from_toml(NO_ATTRS)
    assert config.attrs != {}


def test_no_variables():
    config = Config.from_toml(NO_VARS)
    assert config.variables == {}


def test_no_coords():
    config = Config.from_toml(NO_COORDS)
    assert config.coords == {}


def test_no_variables_name_error():
    with pytest.raises(ValueError):
        Config.from_toml(NO_VAR_NAME)


def test_no_coords_name_error():
    with pytest.raises(ValueError):
        Config.from_toml(NO_COORD_NAME)
