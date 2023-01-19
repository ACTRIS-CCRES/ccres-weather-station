from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import toml

from ccres_weather_station.types import PathLike

DEFAULT_CONFIG = Path(__file__).parent / "config.toml"


@dataclass
class VariableConfig:
    name: str
    standard_name: Optional[str] = None
    long_name: Optional[str] = None
    units: Optional[str] = None
    comment: Optional[str] = None
    instrument: Optional[str] = None
    cell_methods: Optional[str] = None
    dtype: Optional[str] = None


@dataclass
class CoordConfig:
    name: str
    standard_name: Optional[str] = None
    long_name: Optional[str] = None
    units: Optional[str] = None
    calendar: Optional[str] = None


class Config:
    """Configuration object containing metdata.

    - the variables names
    - the default metadata for global attributes
    - the default metadata for variables attributes
    """

    def __init__(
        self,
        variables: Dict[str, VariableConfig],
        coords: Dict[str, CoordConfig],
        attrs: Dict[str, str],
    ):
        self.variables = variables
        self.coords = coords
        self.attrs = attrs

    @classmethod
    def from_toml(cls, path: PathLike) -> "Config":
        path = Path(path)

        d = dict(toml.load(str(path.absolute())))

        # Load variables config
        _variables = d["variables"]["meta"]
        variables = {
            name: VariableConfig(**attrs) for (name, attrs) in _variables.items()
        }

        # Load coords config
        _coords = d["coords"]["meta"]
        coords = {name: CoordConfig(**attrs) for (name, attrs) in _coords.items()}

        global_attrs = d["attrs"]

        return cls(
            variables,
            coords,
            global_attrs,
        )

    @classmethod
    def default(cls) -> "Config":
        return cls.from_toml(DEFAULT_CONFIG)
