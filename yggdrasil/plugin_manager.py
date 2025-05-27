
import os
import importlib.util
import json

class PluginManager:
    def __init__(self, plugin_dir="./plugins"):
        self.plugin_dir = plugin_dir
        os.makedirs(self.plugin_dir, exist_ok=True)
        self.plugins = self.discover_plugins()

    def discover_plugins(self):
        plugins = []
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(self.plugin_dir, file)
                meta_path = path.replace(".py", ".json")
                if os.path.exists(meta_path):
                    with open(meta_path, "r") as f:
                        meta = json.load(f)
                else:
                    meta = {"name": file, "description": "No description"}
                plugins.append({"file": file, "path": path, "meta": meta})
        return plugins

    def list_plugins(self):
        return [(p["meta"].get("name", p["file"]), p["meta"].get("description", "")) for p in self.plugins]

    def run_plugin(self, name):
        plugin = next((p for p in self.plugins if p["file"] == name or p["meta"].get("name") == name), None)
        if not plugin:
            print(f"[!] Plugin '{name}' not found.")
            return
        spec = importlib.util.spec_from_file_location("plugin", plugin["path"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "run"):
            print(f"[+] Running plugin: {plugin['meta'].get('name', plugin['file'])}")
            module.run()
        else:
            print(f"[!] Plugin '{name}' does not have a 'run()' function.")
