
import json
import os

class IntelManager:
    def __init__(self, report_dir=None):
        self.report_dir = report_dir or os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel_file = os.path.join(self.report_dir, "intel.json")
        if not os.path.exists(self.intel_file):
            with open(self.intel_file, "w") as f:
                json.dump({}, f)

    def load(self):
        if os.path.exists(self.intel_file):
            with open(self.intel_file, "r") as f:
                return json.load(f)
        return {}

    def save(self, data):
        with open(self.intel_file, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, module, key, value):
        data = self.load()
        if module not in data:
            data[module] = {}
        data[module][key] = value
        self.save(data)

    def get(self, module, key, default=None):
        data = self.load()
        return data.get(module, {}).get(key, default)

    def get_module_data(self, module):
        data = self.load()
        return data.get(module, {})
