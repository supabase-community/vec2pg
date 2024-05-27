import sys
import os
import json
import importlib


def load_plugins(plugins_dir):
    result = {}
    if len(plugins_dir) > 0 and os.path.exists(plugins_dir):
        for filename in os.listdir(plugins_dir):
            if len(filename) > 0 and filename.endswith('.py') and not filename.startswith('.'):
                module_name, _ = os.path.splitext(filename)
                module = importlib.import_module(f'plugins.{module_name}')
                if module and hasattr(module, 'main'):
                    result[module_name] = module.main
    assert len(result) > 0, "Plugins not found."
    return result


def main():
    if len(sys.argv) != 3:
        print("Usage:\tvec2pg plugin_name 'path/to/config.json'")
        print("Available plugins:\t", tuple(load_plugins('plugins')))
        exit(1)

    plugin_name = sys.argv[1]
    config_file = sys.argv[2]
    if len(plugin_name) > 0 and os.path.exists(config_file):
        plugins = load_plugins('plugins')
        if len(plugins) > 0 and plugin_name in plugins:
            with open(config_file) as f:
                config = json.loads(f.read())
                if plugins[plugin_name](config):
                    print("OK") # WIP


if __name__ in "__main__":
    main()
