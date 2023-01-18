"""Console script for ccres_weather_station."""

import sys

import click


@click.command()
def main(args=None):
    """Console script for ccres_weather_station."""
    click.echo("ccres_weather_station.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
