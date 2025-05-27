"""
Asgard Framework Module
Copyright (c) 2025 The Divinity Project

This module is part of the Asgard Framework. Use is subject to the MIT License
and the disclaimer outlined in LICENSE_Asgard_Framework_Expanded.txt.

Unauthorized or unethical use is strictly prohibited and may violate international law.
Visit: https://opensource.org/licenses/MIT

This file is distributed with ABSOLUTELY NO WARRANTY. Use at your own risk.
"""

from yggdrasil.workspace_manager import WorkspaceManager
import os
import subprocess

class Yggdrasil:
    def __init__(self):
        self.ws = WorkspaceManager()
        self.ws.load_active_workspace()
        self.targets = self.load_targets()
        print("[+] Active Workspace:", self.ws.active)
        print("[+] Loaded Targets:", self.targets)

    def load_targets(self):
        target_file = os.path.join(self.ws.active, "targets.txt")
        if os.path.exists(target_file):
            with open(target_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def run_alpha_module(self, name, target):
        module_path = f"{name}/{name}_alpha.py"
        if os.path.exists(module_path):
            print(f"[+] Running {name}_alpha module on {target}...")
            target_report_path = os.path.join(self.ws.get_path("reports"), target.replace("https://", "").replace("http://", "").replace("/", "_"))
            os.makedirs(target_report_path, exist_ok=True)
            os.environ["ASGARD_REPORTS_DIR"] = target_report_path
            os.environ["ASGARD_INTEL_FILE"] = os.path.join(target_report_path, "intel.json")
            os.environ["ASGARD_TARGET"] = target
            subprocess.run(["python3", module_path])
        else:
            print(f"[!] Module {name}_alpha.py not found.")

    def run_chain(self):
        modules = ["thor", "odin", "freya", "baldur", "njord", "heimdall", "hel", "loki", "mimir", "norns"]
        for target in self.targets:
            print(f"[=] Starting chain for {target}")
            for mod in modules:
                self.run_alpha_module(mod, target)

if __name__ == "__main__":
    ygg = Yggdrasil()
    ygg.run_chain()
