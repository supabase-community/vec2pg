from typer.testing import CliRunner

from vec2pg.cli import app


def test_app_help_does_not_error(cli_runner: CliRunner):
    cli_runner.invoke(app, ["--help"])
