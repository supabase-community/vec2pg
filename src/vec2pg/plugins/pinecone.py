from typing import Annotated

import numpy as np
import psycopg
import typer
from pgvector.psycopg import register_vector
from pinecone import Pinecone
from tqdm import tqdm

app = typer.Typer()

# Env Var Names
PINECONE_API_KEY = "PINECONE_API_KEY"
PINECONE_NAMESPACE = "PINECONE_NAMESPACE"
PINECONE_INDEX = "PINECONE_INDEX"
POSTGRES_CONNECTION_STRING = "POSTGRES_CONNECTION_STRING"
POSTGRES_SCHEMA_NAME = "POSTGRES_SCHEMA_NAME"
POSTGRES_TABLE_NAME = "POSTGRES_TABLE_NAME"


def to_qualified_table_name(pinecone_index: str) -> str:
    table_name = f"{pinecone_index}"
    return f'vec2pg."{table_name}"'


@app.command()
def migrate(
    pinecone_index: str,
    pinecone_api_key: Annotated[str, typer.Argument(envvar=PINECONE_API_KEY)],
    postgres_connection_string: Annotated[
        str, typer.Argument(envvar=POSTGRES_CONNECTION_STRING)
    ],
):
    # Init Pinecone client and index
    client = Pinecone(api_key=pinecone_api_key)
    index = client.Index(pinecone_index)

    index_description = index.describe_index_stats()
    index_namespaces = [key for key in index_description["namespaces"]]
    vector_count = index_description["total_vector_count"]

    # Prep the database with minimal requirements
    conn = psycopg.connect(postgres_connection_string, autocommit=True)
    conn.execute("create extension if not exists vector")
    conn.execute("create schema if not exists vec2pg")

    # Setup the Postgres table
    qualified_name = to_qualified_table_name(pinecone_index)
    conn.execute(f"drop table if exists {qualified_name}")  # type: ignore
    create_table_query = f"create table {qualified_name} (id text, values vector, namespace text, metadata json)"
    conn.execute(create_table_query)  # type: ignore

    # Make psycopg aware of the vector type
    register_vector(conn)

    # Progress bar
    with tqdm(total=vector_count) as pbar:

        for pinecone_namespace in index_namespaces:

            # Iterate through the pinecone index
            for ids in index.list(
                namespace=pinecone_namespace,
                limit=100,
            ):
                batch_result = index.fetch(ids, namespace=pinecone_namespace)
                records = [
                    (
                        rec["id"],
                        np.array(rec["values"]),
                        pinecone_namespace,
                        rec.get("metadata"),
                    )
                    for rec in batch_result.vectors.values()
                ]

                cur = conn.cursor()

                with cur.copy(
                    f"""
                    copy {qualified_name}(id, values, namespace, metadata)
                    from stdin with (format binary)
                    """  # type: ignore
                ) as copy:
                    copy.set_types(["text", "vector", "text", "json"])

                    for rec in records:
                        copy.write_row(rec)

                    while conn.pgconn.flush() == 1:
                        pass

                pbar.update(len(records))

    typer.echo(
        f"Pinecone index {pinecone_index} successfully written to Postgres table "
        + typer.style(
            qualified_name, fg=typer.colors.BLACK, bg=typer.colors.WHITE, bold=True
        )
    )
