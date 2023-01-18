"""The setup script."""
from setuptools import setup

version = {}
with open("ccres_weather_station/__init__.py") as fp:
    exec(fp.read(), version)

setup(version=version["__version__"])
