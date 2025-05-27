"""
Asgard Framework Module
Copyright (c) 2025 The Divinity Project

This module is part of the Asgard Framework. Use is subject to the MIT License
and the disclaimer outlined in LICENSE_Asgard_Framework_Expanded.txt.

Unauthorized or unethical use is strictly prohibited and may violate international law.
Visit: https://opensource.org/licenses/MIT

This file is distributed with ABSOLUTELY NO WARRANTY. Use at your own risk.
"""

import os
import json
import subprocess
import socket
from yggdrasil.intel_manager import IntelManager

class ThorAlpha:
    def __init__(self):
        self.target = os.getenv("ASGARD_TARGET", "localhost")
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.output_file = os.path.join(self.report_dir, "thor_alpha_nmap.xml")

    def resolve_ip(self):
        try:
            return socket.gethostbyname(self.target.replace("http://", "").replace("https://", "").split("/")[0])
        except:
            return self.target

    def run_nmap(self):
        ip = self.resolve_ip()
        print(f"[+] Running Nmap on {ip}...")
        cmd = ["nmap", "-sV", "-p-", "-oX", self.output_file, ip]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.intel.add("thor", "ip", ip)
        self.intel.add("thor", "nmap_scan_complete", True)

    def save_log(self):
        log_path = os.path.join(self.report_dir, "thor_alpha_results.json")
        with open(log_path, "w") as f:
            json.dump({"target": self.target, "nmap_xml": self.output_file}, f, indent=2)

    def run(self):
        self.run_nmap()
        self.save_log()
        print("[+] Thor Alpha completed.")

if __name__ == "__main__":
    ThorAlpha().run()
