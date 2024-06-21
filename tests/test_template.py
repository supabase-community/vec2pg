from typer.testing import CliRunner

from vec2pg.cli import app


def test_app_help_does_not_error():
    runner = CliRunner()
    runner.invoke(app, ["--help"])
