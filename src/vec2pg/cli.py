import typer

from vec2pg.plugins import pinecone, qdrant

# Link to documentation to be shown in the CLI help.
doc_url = "Documentation:\thttps://supabase-community.github.io/vec2pg"

app = typer.Typer(epilog=doc_url)
app.add_typer(pinecone.app, name="pinecone")
app.add_typer(qdrant.app, name="qdrant")

if __name__ == "__main__":
    app()
