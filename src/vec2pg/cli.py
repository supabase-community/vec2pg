import typer

from vec2pg.plugins import pinecone

app = typer.Typer()
app.add_typer(pinecone.app, name="pinecone")

if __name__ == "__main__":
    app()
