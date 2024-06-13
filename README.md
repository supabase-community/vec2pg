# vec2pg

- Simple extendable CLI tool to migrate data into [Supabase](https://supabase.com).


# Use

- `python ./vec2pg.py pinecone "/path/to/config.json"`
- `python ./vec2pg.py --help` for a help message.


# Requisites

- Python >= 3.10
- [Typer-slim](https://typer.tiangolo.com/#typer-slim)
- [Pinecone-client](https://github.com/pinecone-io/pinecone-python-client)
- [Psycopg](https://www.psycopg.org/psycopg3/docs)
- Valid `config.json` file with working [API keys](https://docs.pinecone.io/guides/get-started/quickstart#2-get-your-api-key), etc.


# Dev-Dependencies

- [Pre-commit](https://pre-commit.com)
- [Prospector](https://github.com/PyCQA/prospector)


# Tests

- `python tests/tests.py` from root folder, [see tests folder](https://github.com/supabase-community/vec2pg/tree/main/tests).


# Structure

- `vec2pg.py` main executable file.
- `config.json` user-editable config file, just a JSON.
- `plugins/*.py` plugins, just a Python module.
- `tests/tests.py` tests.


# Extending

- [Minimal noop plugin code](https://github.com/supabase-community/vec2pg/blob/main/tests/tests.py#L17)


# Stars

![](https://starchart.cc/supabase-community/vec2pg.svg)
