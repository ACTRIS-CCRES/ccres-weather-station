"""Tests for `ccres_weather_station` package."""


from pathlib import Path

from click.testing import CliRunner

from ccres_weather_station.cli import cli

INPUT_SIRTA_FILE = Path(
    Path(__file__).parent.parent
    / "data/sirta/meteoairsol_1a_Lz1NairF1minPtuvPrain_v01_20201010_000000_1440.asc"
)

OUTPUT_SIRTA_FILE = Path(Path(__file__).parent.parent / "data/outputs/e2e_sirta.nc")


def test_e2e_sirta():
    """Test the Help argument of CLI."""
    runner = CliRunner()

    result = runner.invoke(
        cli.main,
        [
            "--station",
            "SIRTA",
            "--input-files",
            INPUT_SIRTA_FILE,
            "--output-file",
            OUTPUT_SIRTA_FILE,
        ],
    )
    assert result.exit_code == 0
