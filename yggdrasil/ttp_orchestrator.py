
import os
import json
import time
import subprocess

class TTPOrchestrator:
    def __init__(self, profile_path="./ttp_profiles.json"):
        self.profile_path = profile_path
        self.load_profiles()

    def load_profiles(self):
        if not os.path.exists(self.profile_path):
            self.profiles = {}
        else:
            with open(self.profile_path, "r") as f:
                self.profiles = json.load(f)

    def list_profiles(self):
        return list(self.profiles.keys())

    def run_profile(self, name):
        if name not in self.profiles:
            print(f"[!] TTP profile '{name}' not found.")
            return
        chain = self.profiles[name]
        for step in chain:
            module = step["module"]
            technique = step.get("technique", "unknown")
            delay = step.get("delay", 2)
            print(f"[+] Running {module}_alpha (TTP: {technique})...")
            subprocess.run(["python3", f"{module}/{module}_alpha.py"])
            time.sleep(delay)
