from os import environ
import psycopg
import pytest
import time
import os
import json
from parse import parse
import time

import subprocess
import random
import string
from typing import Generator

from vec2pg.plugins import pinecone


from pinecone.data.index import Index
from pinecone import Pinecone, ServerlessSpec


@pytest.fixture(scope="session")
def postgres_connection_string() -> Generator[str, None, None]:
    yield "postgresql://postgres:password@localhost:5629/v2p"


@pytest.fixture(scope="session")
def maybe_start_pg(postgres_connection_string) -> Generator[None, None, None]:
    """Creates a postgres 12 docker container that can be connected
    to using the PYTEST_DB connection string"""

    container_name = "vec2pg_pg"
    image = "supabase/postgres:15.1.1.68"

    connection_template = "postgresql://{user}:{pw}@{host}:{port:d}/{db}"
    conn_args = parse(connection_template, postgres_connection_string)

    # Don't attempt to instantiate a container if
    # we're on CI
    if "GITHUB_SHA" in os.environ:
        yield
        return

    try:
        is_running = (
            subprocess.check_output(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name]
            )
            .decode()
            .strip()
            == "true"
        )
    except subprocess.CalledProcessError:
        # Can't inspect container if it isn't running
        is_running = False

    if is_running:
        yield
        return

    subprocess.call(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-p",
            f"{conn_args['port']}:5432",  # type: ignore
            "-d",
            "-e",
            f"POSTGRES_DB={conn_args['db']}",  # type: ignore
            "-e",
            f"POSTGRES_PASSWORD={conn_args['pw']}",  # type: ignore
            "-e",
            f"POSTGRES_USER={conn_args['user']}",  # type: ignore
            "--health-cmd",
            "pg_isready",
            "--health-interval",
            "3s",
            "--health-timeout",
            "3s",
            "--health-retries",
            "15",
            image,
        ]
    )
    # Wait for postgres to become healthy
    for _ in range(10):
        out = subprocess.check_output(["docker", "inspect", container_name])
        inspect_info = json.loads(out)[0]
        health_status = inspect_info["State"]["Health"]["Status"]
        if health_status == "healthy":
            break
        else:
            time.sleep(1)
    else:
        raise Exception("Could not reach postgres comtainer. Check docker installation")
    yield
    # subprocess.call(["docker", "stop", container_name])
    return


@pytest.fixture(scope="session")
def cursor(maybe_start_pg: None, postgres_connection_string: str):
    """sqlalchemy engine fixture"""
    maybe_start_pg  # type: ignore
    conn = psycopg.connect(postgres_connection_string)
    cursor = conn.cursor()

    try:
        yield cursor
    finally:
        cursor.close()
        conn.close()


@pytest.fixture(scope="session")
def pinecone_apikey() -> Generator[str, None, None]:
    try:
        yield environ[pinecone.PINECONE_APIKEY]
    except KeyError:
        raise Exception(
            "Pinecone APIKEY required to run the test suite. Create an API key and store it in an environment variable named {pinecone.PINECONE_APIKEY}. A free account is sufficient"
        )


@pytest.fixture(scope="session")
def pinecone_client(pinecone_apikey) -> Pinecone:
    return Pinecone(api_key=pinecone_apikey)


@pytest.fixture(scope="session")
def pinecone_namespace():
    return "ns1"


@pytest.fixture(scope="session")
def pinecone_index_name():
    random_suffix = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    index_name = f"vec2pg-test-ix-{random_suffix}"
    return index_name


@pytest.fixture(scope="session")
def pinecone_index(
    pinecone_client, pinecone_namespace, pinecone_index_name
) -> Generator[Index, None, None]:

    pinecone_client.create_index(
        name=pinecone_index_name,
        dimension=2,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

    index = pinecone_client.Index(pinecone_index_name)

    index.upsert(
        vectors=[
            {"id": "vec1", "values": [1.0, 1.5], "metadata": {"key": "val"}},
            {"id": "vec2", "values": [2.0, 1.0]},
            {"id": "vec3", "values": [0.1, 3.0]},
            {"id": "vec4", "values": [1.0, -2.5]},
            {"id": "vec5", "values": [3.0, -2.0]},
            {"id": "vec6", "values": [0.5, -1.5]},
        ],
        namespace=pinecone_namespace,
    )

    # Indexes are eventually consistent....
    # Required to read your own writes, otherwise
    # tests randomly fail with no data
    for _ in range(100):
        vec_count = index.describe_index_stats()["total_vector_count"]
        if vec_count == 6:
            break

        time.sleep(0.1)
    else:
        raise Exception("Pinecone sample data never loaded")

    try:
        yield index
    finally:
        pinecone_client.delete_index(pinecone_index_name)