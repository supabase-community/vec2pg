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

A CLI for migrating vector workloads from [Pinecone](https://www.pinecone.io/) to [Pgvector](https://github.com/pgvector/pgvector) on [Supabase](https://supabase.com).

Additional data sources will be added soon.

# Use

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

## Pinecone

```
vec2pg pinecone migrate --help
```

```

 Usage: vec2pg pinecone migrate [OPTIONS] PINECONE_APIKEY PINECONE_INDEX                                                 
                                PINECONE_NAMESPACE POSTGRES_CONNECTION_STRING                                            
                                                                                                                         
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    pinecone_apikey                 TEXT  [env var: PINECONE_APIKEY] [default: None] [required]              │
│ *    pinecone_index                  TEXT  [env var: PINECONE_INDEX] [default: None] [required]               │
│ *    pinecone_namespace              TEXT  [env var: PINECONE_NAMESPACE] [default: None] [required]           │
│ *    postgres_connection_string      TEXT  [env var: POSTGRES_CONNECTION_STRING] [default: None] [required]   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


# Requisites
- Python >= 3.8

# Contributing

To run the tests you will need
- Python >= 3.8
- docker
- [Pinecone API key](https://docs.pinecone.io/guides/get-started/authentication#find-your-pinecone-api-key)

The Pinecone API key should be stored as an environment variable `PINECONE_APIKEY`

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
