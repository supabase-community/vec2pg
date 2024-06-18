import enum
import json
from pathlib import Path

import typer  # pip install typer-slim

from vec2pg.plugins import pinecone

app = typer.Typer()


class Plugin(str, enum.Enum):
    pinecone = "pinecone"


@app.command()
def main(plugin: Plugin, config_json: Path = typer.Argument(..., exists=True)):
    # Load config
    with open(config_json) as f:
        config = json.load(f)

    # Run plugin with config
    if plugin == Plugin.pinecone:
        pinecone.main(config[plugin])
    else:
        raise typer.BadParameter(f"Unknown plugin {plugin}")


if __name__ == "__main__":
    app()
