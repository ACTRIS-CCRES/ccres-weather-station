# Command Line interface

```{eval-rst}
.. automodule:: ccres_weather_station.cli.cli
   :members:
```
## Usage
```shell
Usage: ccres_weather_station [OPTIONS]

  Command line interface for ccres_weather_station.

Options:
  -v, --verbose            Set the level of verbosity. By default ERROR.
                           -v sets the level to INFO.
                           -vv sets the level to DEBUG.
  --start-date [%Y-%m-%d]  Date from which to keep all output data.
                           See also --end-date for the reciprocal
  --end-date [%Y-%m-%d]    Date from which to remove all output data.
                           See also --start-date for the reciprocal
  --station TEXT           Station name  [required]
  --input-files PATH       File(s) to treat  [required]
  --output-file PATH       Output file to be written  [required]
  -h, --help               Show this message and exit.
```
