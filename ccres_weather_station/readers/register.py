from typing import Dict, Type

from ccres_weather_station.readers.base import BaseReader
from ccres_weather_station.readers.sirta import SirtaReader

READERS: Dict[str, Type[BaseReader]] = {}


def register_reader(reader: Type[BaseReader], name: str) -> None:
    if not issubclass(reader, BaseReader) or reader.__abstractmethods__ != frozenset():
        raise TypeError(f"Reader {reader.__name__} is not implementing BaseReader")
    READERS[name.lower()] = reader


def get_reader_class(station_name: str) -> Type[BaseReader]:
    if station_name.lower() not in READERS.keys():
        raise ValueError(
            f"{station_name} reader not found. "
            f"Available readers are {list(READERS.keys())}"
        )
    return READERS[station_name.lower()]


register_reader(SirtaReader, "sirta")
