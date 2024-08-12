# `vec2pg`

<p>
    <a href="https://github.com/supabase-community/vec2pg/actions">
        <img src="https://github.com/supabase-community/vec2pg/workflows/tests/badge.svg" alt="Test Status" height="18">
    </a>
    <a href="https://github.com/supabase-community/vec2pg/actions">
        <img src="https://github.com/supabase-community/vec2pg/workflows/pre-commit/badge.svg" alt="Pre-commit Status" height="18">
    </a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python version" height="18"></a>
    <a href=""><img src="https://img.shields.io/badge/postgresql-15+-blue.svg" alt="PostgreSQL version" height="18"></a>
</p>
<p>
    <a href="https://github.com/supabase-community/vec2pg/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/markdown-subtemplate.svg" alt="License" height="18"></a>
    <a href="https://badge.fury.io/py/alembic_utils"><img src="https://badge.fury.io/py/vec2pg.svg" alt="PyPI version" height="18"></a>
    <a href="https://github.com/psf/black">
      <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Codestyle Black" height="18">
    </a>
    <a href="https://pypi.org/project/vec2pg/"><img src="https://img.shields.io/pypi/dm/vec2pg.svg" alt="Download count" height="18"></a>
</p>

---

**Documentation**: <a href="https://supabase-community.github.io/vec2pg" target="_blank">https://supabase-community.github.io/vec2pg</a>

**Source Code**: <a href="https://github.com/supabase-community/vec2pg" target="_blank">https://github.com/supabase-community/vec2pg</a>

---

`vec2pg` is a CLI for migrating data from third party vector databases to [Supabase](https://supabase.com).


Supported data sources include:

- [Pinecone](pinecone.md)
- [Qdrant](qdrant.md)
- [[Vote for others]](https://github.com/supabase-community/vec2pg/issues/6)

The general flow involves passing an API key for your vector database, a Postgres connection string, and a reference to the collection you want to copy. `vec2pg` then presents a progress bar in the terminal that you can use to monitor progress. Once complete, the vectors and any associated metadata are available in your Postgres instance at `vec2pg.<collection_name>`.


### Usage

```
vec2pg --help
```

```                                                                                                                                           
 Usage: vec2pg [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                         
╭─ Options ──────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.│
│ --show-completion             Show completion for the current shell    │
│ --help                        Show this message and exit.              │
╰────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────╮
│ pinecone                      Move data from Pinecone to Supabase      │
│ qdrant                        Move data from Qdrant to Supabase        │
╰────────────────────────────────────────────────────────────────────────╯
```


