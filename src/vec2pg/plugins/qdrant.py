from typing import Annotated

import numpy as np
import psycopg
import typer
from pgvector.psycopg import register_vector
from tqdm import tqdm
from qdrant_client import QdrantClient
from vec2pg.common import POSTGRES_CONNECTION_STRING

app = typer.Typer()

# Env Var Names
QDRANT_API_KEY = "QDRANT_API_KEY"


def to_qualified_table_name(collection_name: str) -> str:
    assert '"' not in collection_name
    return f'vec2pg."{collection_name}"'


@app.command()
def migrate(
    qdrant_collection_name: str,
    qdrant_url: str,
    qdrant_api_key: Annotated[str, typer.Argument(envvar=QDRANT_API_KEY)],
    postgres_connection_string: Annotated[
        str, typer.Argument(envvar=POSTGRES_CONNECTION_STRING)
    ],
):

    # Init Pinecone client and index
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    if not client.collection_exists(collection_name=qdrant_collection_name):
        raise Exception("Requested Qdrant collection does not exist")

    vector_count = client.count(collection_name=qdrant_collection_name).count

    if vector_count == 0:
        raise Exception("No records present in requested Qdrant collection")

    # Prep the database with minimal requirements
    conn = psycopg.connect(postgres_connection_string, autocommit=True)
    conn.execute("create extension if not exists vector")
    conn.execute("create schema if not exists vec2pg")

    # Setup the Postgres table
    qualified_name = to_qualified_table_name(qdrant_collection_name)
    conn.execute(f"drop table if exists {qualified_name}")  # type: ignore
    create_table_query = f"create table {qualified_name} (id bigint, values vector, metadata json, shard_key text, order_value text)"
    conn.execute(create_table_query)  # type: ignore

    # Make psycopg aware of the vector type
    register_vector(conn)

    limit = 100
    offset = 0

    # Progress bar
    with tqdm(total=vector_count) as pbar:

        while True:

            batch_result = client.scroll(
                collection_name=qdrant_collection_name,
                with_payload=True,
                with_vectors=True,
                limit=limit,
                offset=offset,
            )

            if batch_result is None:
                # No more results
                break

            batch_records, _ = batch_result

            batch_size = len(batch_records)

            if batch_size == 0:
                # no more records
                break

            offset += batch_size

            records = [
                (
                    rec.id,
                    np.array(rec.vector),
                    rec.payload,
                    str(rec.shard_key),
                    str(rec.order_value),
                )
                for rec in batch_records
            ]

            cur = conn.cursor()

            with cur.copy(
                f"""
                copy {qualified_name}(id, values, metadata, shard_key, order_value)
                from stdin with (format binary)
                """  # type: ignore
            ) as copy:
                copy.set_types(["bigint", "vector", "json", "text", "text"])

                for rec in records:
                    copy.write_row(rec)

                while conn.pgconn.flush() == 1:
                    pass

            pbar.update(len(records))

    typer.echo(
        f"Qdrant collection {qdrant_collection_name} successfully written to Postgres table "
        + typer.style(
            qualified_name, fg=typer.colors.BLACK, bg=typer.colors.WHITE, bold=True
        )
    )
