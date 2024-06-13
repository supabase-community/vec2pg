import json

import psycopg                 # pip install psycopg[binary]
from pinecone import Pinecone  # pip install pinecone-client


def _get_index_data(index, namespace, ids):
    """Fetch data from the Pinecone index"""
    return index.fetch(namespace=namespace, ids=ids)


def _load_vectors(index, namespace, pagination_token=None):
    """Get vectors from the Pinecone index"""
    return index.list_paginated(namespace=namespace, pagination_token=pagination_token)


def _load_dimensions(index):
    """Get dimensions from the Pinecone index"""
    return index.describe_index_stats()["dimension"]


def _create_connection(database_config):
    """Connect to the database"""
    hostname = database_config.get("hostname")
    username = database_config.get("username")
    database = database_config.get("database")
    password = database_config.get("password")
    port = database_config.get("port")
    return psycopg.connect(
        f"host={hostname} dbname={database} user={username} password={password} port={port}"
    )


def _create_embedding_tables(cursor, table_name, dimension):
    """Create tables for embeddings"""
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}_json_embeddings;")
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}_vector_embeddings;")
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name}_json_embeddings (model jsonb);"
    )
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name}_vector_embeddings ( model float array[{dimension}], label jsonb);"
    )


def _load_embeddings(cursor, table_name, json_data, dimension):
    """Load embeddings into JSON"""
    with cursor.copy(f"COPY {table_name}_json_embeddings FROM STDIN") as copy:
        copy.set_types(["jsonb"])
        copy.write_row([json_data])


def _cleanup_embedding_table(cursor, table_name, dimension):
    """Clean up embedding table, insert embeddings into vector table"""
    script = f"insert into {table_name}_vector_embeddings select array(select jsonb_array_elements_text(js.value[0]))::float[{dimension}], js.value[1] from {table_name}_json_embeddings p cross join lateral jsonb_each(p.model::jsonb) js;"
    cursor.execute(script)
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}_json_embeddings;")


def main(config):
    result = False
    try:
        # Get config
        apikey = config.get("apikey")
        namespace = config.get("namespace")
        pinecone_index = config.get("index")
        database_config = {
            "table_name": config.get("table_name"),
            "hostname": config.get("hostname"),
            "username": config.get("username"),
            "database": config.get("database"),
            "password": config.get("password"),
            "port": config.get("port"),
        }

        # Init Pinecone client and index
        client = Pinecone(api_key=apikey)
        index = client.Index(pinecone_index)

        # Load vectors from Pinecone index
        json_batch = dict()
        result_set = _load_vectors(index, namespace)
        while len(result_set.vectors) > 0:
            vectors = (item.id for item in result_set["vectors"])
            batch = _get_index_data(index, namespace, list(vectors))
            json_batch.update(
                {
                    v["id"]: [v["values"], v["metadata"]]
                    for k, v in batch.vectors.items()
                }
            )

            if result_set.pagination:
                result_set = _load_vectors(index, namespace, result_set.pagination.next)
            else:
                break

        dimension = _load_dimensions(index)
        table = database_config["table_name"]

        # Create a connection and cursor to database
        conn = _create_connection(database_config)
        cursor = conn.cursor()

        # Create table for embeddings
        _create_embedding_tables(cursor, table, dimension)
        conn.commit()

        # Load embeddings into JSON table
        _load_embeddings(cursor, table, json.dumps(json_batch), dimension)
        conn.commit()

        # Move embeddings from JSON table to vector table
        cursor = conn.cursor()
        _cleanup_embedding_table(cursor, table, dimension)
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

    except Exception:
        # Something went wrong.
        result = False
    else:
        # Everything went OK.
        result = True
    finally:
        return result
