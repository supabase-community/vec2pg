import importlib
import json
import os

import typer  # pip install typer-slim


def load_plugins(plugins_dir: str) -> dict:
    """Function to load plugins from a directory."""
    result = {}
    # Check if plugins directory exists
    if len(plugins_dir) > 0 and os.path.exists(plugins_dir):
        # Loop files in directory
        for filename in os.listdir(plugins_dir):
            if (
                len(filename) > 0
                and filename.endswith(".py")
                and not filename.startswith(".")
            ):
                # Import modules and add to result dict.
                module_name, _ = os.path.splitext(filename)
                module = importlib.import_module(f"plugins.{module_name}")
                if module and hasattr(module, "main"):
                    result[module_name] = module.main

    assert len(result) > 0, f"Plugins not found: {plugins_dir}"
    return result


def main(plugin_name: str, config_json: str):
    """Main entry func"""
    # Validate args
    assert len(plugin_name) > 0, "Plugin name must not be empty string."
    assert os.path.exists(config_json), f"Config file not found: {config_json}"
    plugin_name = plugin_name.strip().lower()

    # Load plugins
    plugins = load_plugins("plugins")
    assert plugin_name in plugins, f"Plugin not found: {plugin_name}"
    print("Available plugins:\t", tuple(load_plugins("plugins")))

    # Load config
    with open(config_json) as f:
        config = json.load(f)
        # Run plugin with config
        plugins[plugin_name](config[plugin_name])


if __name__ == "__main__":
    typer.run(main)
