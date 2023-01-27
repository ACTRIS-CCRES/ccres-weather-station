"""Console script for ccres_weather_station."""

import datetime as dt
import logging
import sys

import click

from ccres_weather_station.logger import get_log_level_from_count, init_logger
from ccres_weather_station.types import PathLike, PathsLike

lgr = logging.getLogger(__name__)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    type=int,
    help=(
        "\b\nSet the level of verbosity. By default ERROR.\n"
        "-v sets the level to INFO.\n"
        "-vv sets the level to DEBUG."
    ),
)
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help=(
        "\b\nDate from which to keep all output data.\n"
        "See also --end-date for the reciprocal"
    ),
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help=(
        "\b\nDate from which to remove all output data.\n"
        "See also --start-date for the reciprocal"
    ),
)
@click.option(
    "--station",
    type=str,
    required=True,
    help=("\b\nStation name"),
)
@click.option(
    "--input-files",
    type=click.Path(exists=True),
    required=True,
    multiple=True,
    help=("\b\nFile(s) to treat"),
)
@click.option(
    "--output-file",
    type=click.Path(),
    required=True,
    help=("\b\nOutput file to be written"),
)
def main(
    verbose: int,
    start_date: dt.datetime,
    end_date: dt.datetime,
    station: str,
    input_files: PathsLike,
    output_file: PathLike,
) -> int:
    """Command line interface for ccres_weather_station."""
    log_level = get_log_level_from_count(verbose)
    init_logger(log_level)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
