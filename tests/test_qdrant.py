import warnings

from qdrant_client import QdrantClient
from typer.testing import CliRunner

from vec2pg.cli import app
from vec2pg.plugins.qdrant import to_qualified_table_name


def test_pinecone_subcommand_does_not_error() -> None:
    runner = CliRunner()
    runner.invoke(app, ["qdrant", "--help"])


def test_client_is_good(qdrant_client: QdrantClient) -> None:
    assert qdrant_client is not None


def test_client_count(qdrant_client: QdrantClient, qdrant_collection_name) -> None:
    count_response = qdrant_client.count(collection_name=qdrant_collection_name)
    assert count_response.count == 100


def test_qdrant_migrate(
    qdrant_client: QdrantClient,
    qdrant_collection_name: str,
    postgres_connection_string: str,
    cursor,
    cli_runner: CliRunner,
) -> None:
    assert qdrant_client

    with warnings.catch_warnings():
        # Ignore warning about passing an empty API Key since its local
        warnings.simplefilter("ignore")

        result = cli_runner.invoke(
            app,
            [
                "qdrant",
                "migrate",
                qdrant_collection_name,
                "http://localhost:6333",
                "",  # no API key needed in :memory: mode
                postgres_connection_string,
            ],
        )

    print(result.stdout)
    assert result.exit_code == 0

    qualified_name = to_qualified_table_name(qdrant_collection_name)

    recs = cursor.execute(
        f"select id, values, metadata from {qualified_name}"
    ).fetchall()
    assert len(recs) == 100
