import typer

from vec2pg.plugins import pinecone, qdrant

app = typer.Typer()
app.add_typer(pinecone.app, name="pinecone")
app.add_typer(qdrant.app, name="qdrant")

if __name__ == "__main__":
    app()
