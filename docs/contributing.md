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
