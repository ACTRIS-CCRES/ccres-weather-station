"""Tests for `ccres_weather_station` package."""


from click.testing import CliRunner

from ccres_weather_station.cli import cli


def test_command_line_interface_help():
    """Test the Help argument of CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output
