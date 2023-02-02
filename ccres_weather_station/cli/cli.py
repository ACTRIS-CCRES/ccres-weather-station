"""Console script for ccres_weather_station."""

import datetime as dt
import logging
import sys
from pathlib import Path
from typing import Optional, Tuple

import click

from ccres_weather_station.bounders.apply_bounds import apply_bounds
from ccres_weather_station.config.config import Config
from ccres_weather_station.logger import get_log_level_from_count, init_logger
from ccres_weather_station.readers.register import get_reader_class
from ccres_weather_station.types import PathLike, PathsLike
from ccres_weather_station.writers.write import write_nc

lgr = logging.getLogger(__name__)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def _get_dates(
    start_date: Optional[dt.datetime], end_date: Optional[dt.datetime]
) -> Tuple[Optional[dt.datetime], Optional[dt.datetime]]:
    if start_date is not None:
        if end_date is not None:
            if start_date > end_date:
                raise ValueError("Start date is newer than end_date")
            elif start_date == end_date:
                end_date = start_date + dt.timedelta(days=1)
        else:
            end_date = start_date + dt.timedelta(days=1)
    return start_date, end_date


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
    start_date: Optional[dt.datetime],
    end_date: Optional[dt.datetime],
    station: str,
    input_files: PathsLike,
    output_file: PathLike,
) -> int:
    """Command line interface for ccres_weather_station."""
    log_level = get_log_level_from_count(verbose)
    init_logger(log_level)

    start_date, end_date = _get_dates(start_date, end_date)
    output_file = Path(output_file)
    input_files = [Path(input_file) for input_file in input_files]

    lgr.debug("Get reader class")
    reader_class = get_reader_class(station)

    lgr.debug("Get configuration")
    config = Config.default()

    lgr.debug("Instantiate class")
    reader = reader_class(config)

    lgr.debug("Read files")
    ds = reader.read_files(input_files)

    lgr.debug("Apply bound to dataset")
    ds = apply_bounds(ds, config, start_date, end_date)

    lgr.debug("Write dataset")
    write_nc(ds, config, output_file)
    lgr.info(f"Output file {output_file.absolute()} generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
