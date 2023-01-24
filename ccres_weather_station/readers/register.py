from typing import Dict, Type

from ccres_weather_station.readers.base import BaseReader

READERS: Dict[str, Type[BaseReader]] = {}


def register_reader(reader: Type[BaseReader], name: str) -> None:
    if not issubclass(reader, BaseReader) or reader.__abstractmethods__ != frozenset():
        raise TypeError(f"Reader {reader.__name__} is not implementing BaseReader")
    READERS[name.lower()] = reader
