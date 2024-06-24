# vec2pg


<p>
    <a href="https://github.com/supabase-community/vec2pg/actions">
        <img src="https://github.com/supabase-community/vec2pg/workflows/tests/badge.svg" alt="Test Status" height="18">
    </a>
    <a href="https://github.com/supabase-community/vec2pg/actions">
        <img src="https://github.com/supabase-community/vec2pg/workflows/pre-commit/badge.svg" alt="Pre-commit Status" height="18">
    </a>
</p>
<p>
    <a href="https://github.com/supabase-community/vec2pg/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/markdown-subtemplate.svg" alt="License" height="18"></a>
    <a href="https://badge.fury.io/py/alembic_utils"><img src="https://badge.fury.io/py/vec2pg.svg" alt="PyPI version" height="18"></a>
    <a href="https://github.com/psf/black">
      <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Codestyle Black" height="18">
    </a>
    <a href="https://pypi.org/project/vec2pg/"><img src="https://img.shields.io/pypi/dm/vec2pg.svg" alt="Download count" height="18"></a>
</p>
<p>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python version" height="18"></a>
    <a href=""><img src="https://img.shields.io/badge/postgresql-14+-blue.svg" alt="PostgreSQL version" height="18"></a>
</p>

---

**Source Code**: <a href="https://github.com/supabase-community/vec2pg" target="_blank">https://github.com/supabase-community/vec2pg</a>

---

A CLI for migrating data from vector databases to [Supabase](https://supabase.com).

Supported data sources include:
- [Pinecone](https://docs.pinecone.io/home)
- (more soon)


```
vec2pg --help
```

```                                                                                                                                           
 Usage: vec2pg [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                         
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                        │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation. │
│ --help                        Show this message and exit.                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ pinecone                                                                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Migration Guide

### Pinecone

```
vec2pg pinecone migrate --help
```

```
 Usage: vec2pg pinecone migrate [OPTIONS] PINECONE_INDEX PINECONE_API_KEY                                                                      
                                POSTGRES_CONNECTION_STRING                                                                                    
                                                                                                                                              
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    pinecone_index                  TEXT  [default: None] [required]                                        │
│ *    pinecone_api_key                 TEXT  [env var: PINECONE_API_KEY] [default: None] [required]           │
│ *    postgres_connection_string      TEXT  [env var: POSTGRES_CONNECTION_STRING] [default: None] [required]  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```



To migrate from [Pinecone serverless](https://www.pinecone.io/blog/serverless/) index to Postgres you'll need:  

- A Pinecone API Key

![pinecone api key](/assets/pinecone_api_key.png)

- The Pinecone serverless index name

![pinecone serverless index name](/assets/pinecone_index_name.png)

- A Supabase instance

From the Supabase instance we need the connection parameters. Retrive them [here](https://supabase.com/dashboard/project/_/settings/database)

![supabsae connection parameters](/assets/supabase_connection_params.png)

And substitute those values into a valid Postgres connection string
```
postgresql://<User>:<Password>@<Host>:<Port>/postgres
```
e.g.
```
postgresql://postgres.ahqsutirwnsocaaorimo:<Password>@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Then we can call `vec2pg pinecone migrate` passing our values. You can supply all parameters directly to the CLI, but its a good idea to pass the Pinecone API Key (PINECONE_API_KEY) and Supabase connection string (POSTGRES_CONNECTION_STRING) as environment variables to avoid logging credentials to your shell's history.

![sample output](/assets/pinecone_to_supabase_output.png)

The CLI provies a progress bar to monitor the migration.

On completion, you can view a copy of the Pinecone index data in Supabase Postgres at `vec2pg.<pinecone index name>`

![view results](/assets/view_results.png)

From there you can transform and manipulate the data in Postgres using SQL.


# Requisites
- Python >= 3.8

# Contributing

To run the tests you will need
- Python >= 3.8
- docker
- [Pinecone API key](https://docs.pinecone.io/guides/get-started/authentication#find-your-pinecone-api-key)

The Pinecone API key should be stored as an environment variable `PINECONE_API_KEY`

Run the tests
```
poetry run pytest
```

Run the pre-commit hooks
```
poetry run pre-commit run --all
```

# Star History

![](https://starchart.cc/supabase-community/vec2pg.svg)
