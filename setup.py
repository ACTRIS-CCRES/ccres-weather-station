"""The setup script."""
from typing import Dict

from setuptools import setup

version: Dict[str, str] = {}
with open("ccres_weather_station/__init__.py") as fp:
    exec(fp.read(), version)

setup(version=version["__version__"])
