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

A CLI for migrating vector workloads from [pinecone](https://www.pinecone.io/) to [pgvector](https://github.com/pgvector/pgvector) on [Supabase](https://supabase.com).

Additional data sources will be added soon.

# Use

- `vec2pg.py --help` for a help message.
```                                                                                                                                           
 Usage: vec2pg [OPTIONS] PLUGIN:{pinecone} CONFIG_JSON                                                                                       
                                                                                                                                             
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    plugin           PLUGIN:{pinecone}  [default: None] [required]                                             │
│ *    config_json      PATH               [default: None] [required]                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.  │
│ --help                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


- `vec2pg pinecone "/path/to/config.json"`


# Requisites

- Python >= 3.8
- Valid `config.json` file with working [API keys](https://docs.pinecone.io/guides/get-started/quickstart#2-get-your-api-key), etc.


# Contributing

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
