# Contributing

`vec2pg` is open source software. External contributions are welcome. Note that we have a high bar for testing.

Before opening a PR, please [create an issue](https://github.com/supabase-community/vec2pg/issues/new/choose) in GitHub to discuss and approve the change you're interested in making.

To run the tests you will need:

- Python >= 3.8
- Docker
- [Pinecone API key](https://docs.pinecone.io/guides/get-started/authentication#find-your-pinecone-api-key) - pinecone does not support a local mode, so we have to hit their service during testing

The Pinecone API key should be stored as an environment variable `PINECONE_API_KEY`

Run the tests
```
poetry run pytest
```

Run the pre-commit hooks
```
poetry run pre-commit run --all
```
