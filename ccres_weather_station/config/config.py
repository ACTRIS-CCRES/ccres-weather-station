import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterator, Optional, Tuple

import toml

from ccres_weather_station.types import PathLike

lgr = logging.getLogger(__name__)
DEFAULT_CONFIG = Path(__file__).parent / "default.toml"


@dataclass(repr=True)
class VariableMeta:
    standard_name: Optional[str] = None
    long_name: Optional[str] = None
    units: Optional[str] = None
    comment: Optional[str] = None
    instrument: Optional[str] = None
    cell_methods: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(asdict(self).items())


@dataclass(repr=True)
class VariableEncoding:
    """xarray encoding wrapper for variables.

    Notes
    -----
        The dtype must be numpy-like but without the np.
        So instead of np.float32, we need float32

    Notes
    -----
        See https://docs.xarray.dev/en/stable/user-guide/io.html\
            #reading-encoded-data
    """

    zlib: Optional[bool] = None
    shuffle: Optional[bool] = None
    complevel: Optional[int] = None
    fletcher32: Optional[bool] = None
    contiguous: Optional[bool] = None
    chunksizes: Optional[int] = None
    dtype: Optional[str] = None
    units: Optional[str] = None
    calendar: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(asdict(self).items())


@dataclass(repr=True)
class VariableConfig:
    name: str
    meta: VariableMeta
    encoding: VariableEncoding


@dataclass(repr=True)
class CoordMeta:
    standard_name: Optional[str] = None
    long_name: Optional[str] = None
    units: Optional[str] = None
    calendar: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(asdict(self).items())


@dataclass(repr=True)
class CoordEncoding:
    """xarray encoding wrapper for coordinates.

    Notes
    -----
        The dtype must be numpy-like but without the np.
        So instead of np.float32, we need float32

    Notes
    -----
        See https://docs.xarray.dev/en/stable/user-guide/io.html\
            #reading-encoded-data
    """

    zlib: Optional[bool] = None
    shuffle: Optional[bool] = None
    complevel: Optional[int] = None
    fletcher32: Optional[bool] = None
    contiguous: Optional[bool] = None
    chunksizes: Optional[int] = None
    dtype: Optional[str] = None
    units: Optional[str] = None
    calendar: Optional[str] = None

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(asdict(self).items())


@dataclass(repr=True)
class CoordConfig:
    name: str
    meta: CoordMeta
    encoding: CoordEncoding


@dataclass()
class Config:
    """Configuration object containing metdata.

    - the variables names
    - the default metadata for global attributes
    - the default metadata for variables attributes
    """

    variables: Dict[str, VariableConfig]
    coords: Dict[str, CoordConfig]
    attrs: Dict[str, str]

    @staticmethod
    def _get_meta_var(d: Dict) -> Dict[str, VariableConfig]:
        _variables: Dict[str, VariableConfig] = {}
        if "variables" not in d:
            lgr.warning("No 'variables' section found in configuration file")
            return _variables

        for var in d["variables"]:
            if "name" not in d["variables"][var]:
                raise ValueError(
                    (
                        "Each variable description need a name."
                        f"No name for variables.{var}"
                    )
                )
            var_meta: VariableMeta = VariableMeta()
            if "meta" in d["variables"][var]:
                var_meta = VariableMeta(**d["variables"][var]["meta"])

            var_encoding: VariableEncoding = VariableEncoding()
            if "encoding" in d["variables"][var]:
                var_encoding = VariableEncoding(**d["variables"][var]["encoding"])

            _variables[var] = VariableConfig(
                name=d["variables"][var]["name"],
                meta=var_meta,
                encoding=var_encoding,
            )
        return _variables

    @staticmethod
    def _get_meta_coord(d: Dict) -> Dict[str, CoordConfig]:
        _coords: Dict[str, CoordConfig] = {}
        if "coords" not in d:
            lgr.warning("No 'coords' section found in configuration file")
            return _coords

        for coord in d["coords"]:
            if "name" not in d["coords"][coord]:
                raise ValueError(
                    (
                        "Each coordinate description need a name."
                        f"No name for coords.{coord}"
                    )
                )
            coord_meta: CoordMeta = CoordMeta()
            if "meta" in d["coords"][coord]:
                coord_meta = CoordMeta(**d["coords"][coord]["meta"])

            coord_encoding: CoordEncoding = CoordEncoding()
            if "encoding" in d["coords"][coord]:
                coord_encoding = CoordEncoding(**d["coords"][coord]["encoding"])

            _coords[coord] = CoordConfig(
                name=d["coords"][coord]["name"],
                meta=coord_meta,
                encoding=coord_encoding,
            )
        return _coords

    @staticmethod
    def _get_global_attrs(d: Dict) -> Dict[str, str]:
        attrs = {}
        if "attrs" in d:
            attrs = d["attrs"]
        return attrs

    @classmethod
    def from_toml(cls, path: PathLike) -> "Config":
        """Class method handling the creation of the object.

        It creates the object from a valid Toml configuration file


        Parameters
        ----------
        path : PathLike
            Path of the Toml file

        Returns
        -------
        Config
            The interpretation of the Toml file
        """
        path = Path(path)

        d = dict(toml.load(str(path.absolute())))

        variables: Dict[str, VariableConfig] = cls._get_meta_var(d)
        coords: Dict[str, CoordConfig] = cls._get_meta_coord(d)
        global_attrs = cls._get_global_attrs(d)

        return cls(
            variables,
            coords,
            global_attrs,
        )

    @classmethod
    def default(cls) -> "Config":
        """Create the object from a default config file.

        It creates the object from a valid default Toml file

        Returns
        -------
        Config
            The interpretation of the Toml file
        """
        return cls.from_toml(DEFAULT_CONFIG)

    def _add_other_var(self, other: "Config") -> None:
        for var in other.variables:
            if var not in self.variables:
                self.variables[var] = other.variables[var]
                continue
            for key, value in other.variables[var].meta:
                if value is None:
                    continue
                setattr(
                    self.variables[var].meta,
                    key,
                    getattr(other.variables[var].meta, key),
                )
            for key, value in other.variables[var].encoding:
                if value is None:
                    continue
                setattr(
                    self.variables[var].encoding,
                    key,
                    getattr(other.variables[var].encoding, key),
                )

    def _add_other_coord(self, other: "Config") -> None:
        for coord in other.coords:
            if coord not in self.coords:
                self.coords[coord] = other.coords[coord]
                continue
            for key, value in other.coords[coord].meta:
                if value is None:
                    continue
                setattr(
                    self.coords[coord].meta,
                    key,
                    getattr(other.coords[coord].meta, key),
                )
            for key, value in other.coords[coord].encoding:
                if value is None:
                    continue
                setattr(
                    self.coords[coord].encoding,
                    key,
                    getattr(other.coords[coord].encoding, key),
                )

    def _add_other_attrs(self, other: "Config") -> None:
        for key, attr in other.attrs.items():
            if attr is not None:
                self.attrs[key] = attr

    def add_config_from_toml(self, path: PathLike) -> "Config":
        """Integrate another config file to object.

        The new file have precedence over the old one. That say, if a field
        already exists in the object and is present in the incoming config
        file, it will be overwrited

        Parameters
        ----------
        path : PathLike
            Path of the Toml file

        Returns
        -------
        Config
            Updated config file
        """
        path = Path(path)
        other = Config.from_toml(path)

        self._add_other_var(other)
        self._add_other_coord(other)
        self._add_other_attrs(other)

        return self
