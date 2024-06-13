import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.getcwd())

import vec2pg


class TestVec2Pg(unittest.TestCase):

    def test_valid_plugins(self):
        plugins_dir = "plugins"

        # Create 2 valid plugins
        plugin_code = "def main(config):\n\treturn True\n"  # Minimal noop.
        with open(os.path.join(plugins_dir, "plugin1.py"), "w") as f:
            f.write(plugin_code)
        with open(os.path.join(plugins_dir, "plugin2.py"), "w") as f:
            f.write(plugin_code)

        plugins = vec2pg.load_plugins(plugins_dir)
        print(plugins)
        assert isinstance(plugins, dict)
        assert len(plugins) >= 3
        self.assertIn("plugin1", plugins)
        self.assertIn("plugin2", plugins)
        self.assertIn("pinecone", plugins)

        # Check loaded functions
        for name, func in plugins.items():
            self.assertEqual(func.__name__, "main")

        # Cleanup
        try:
            os.remove(os.path.join(plugins_dir, "plugin1.py"))
            os.remove(os.path.join(plugins_dir, "plugin2.py"))
        except:
            pass

    @patch("vec2pg.load_plugins")
    def test_main_call(self, mock_load_plugins):
        plugin_name = "myplugin"
        config_json = "config.json"
        mock_load_plugins.return_value = {"myplugin": lambda _: None}
        expected_available_plugins = tuple(mock_load_plugins())
        print(expected_available_plugins)
        assert plugin_name in expected_available_plugins


if __name__ == "__main__":
    unittest.main()
