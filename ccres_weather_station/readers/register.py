from typing import Dict

from ccres_weather_station.readers.base import BaseReader

READERS: Dict[str, BaseReader] = {}


def register_reader(reader: BaseReader, name: str):
    if (
        not issubclass(reader, BaseReader)
        or reader.__abstractmethods__ != frozenset()
    ):
        raise TypeError(
            f"Reader {reader.__name__} is not implementing BaseReader"
        )
    READERS[name.lower()] = reader
    print(READERS)
