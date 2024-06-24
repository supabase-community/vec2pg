from os import environ

from pinecone import Pinecone
from pinecone.data.index import Index
from typer.testing import CliRunner

from vec2pg.cli import app
from vec2pg.plugins.pinecone import PINECONE_APIKEY, to_qualified_table_name


def test_pinecone_subcommand_does_not_error() -> None:
    runner = CliRunner()
    runner.invoke(app, ["pinecone", "--help"])


def test_client_is_good(pinecone_client: Pinecone) -> None:
    assert pinecone_client is not None


def test_index_is_good(pinecone_index: Index) -> None:
    assert pinecone_index.describe_index_stats()["dimension"] == 2


def test_pinecone_migrate(
    pinecone_index_name: str,
    postgres_connection_string: str,
    cursor,
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(
        app,
        [
            "pinecone",
            "migrate",
            pinecone_index_name,
            environ[PINECONE_APIKEY],
            postgres_connection_string,
        ],
    )

    print(result.stdout)
    assert result.exit_code == 0

    qualified_name = to_qualified_table_name(pinecone_index_name)

    recs = cursor.execute(
        f"select id, values, metadata from {qualified_name}"
    ).fetchall()
    assert len(recs) == 6
