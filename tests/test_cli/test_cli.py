"""Tests for `ccres_weather_station` package."""

import os

from click.testing import CliRunner

from ccres_weather_station.cli import cli


def test_command_line_interface_help():
    """Test the Help argument of CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output


def test_command_line_interface_minimal():
    """Test the Help argument of CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem() as tmp_dir:
        input_path = os.path.join(tmp_dir, "input.txt")
        output_path = os.path.join(tmp_dir, "output.nc")
        # Create dummy file
        with open(input_path, "w") as fp:
            fp.write("Test line")

        result = runner.invoke(
            cli.main,
            [
                "--station",
                "SIRTA",
                "--input-files",
                input_path,
                "--output-file",
                output_path,
            ],
        )
    assert result.exit_code == 0
