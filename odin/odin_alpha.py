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
import socket
import requests
from yggdrasil.intel_manager import IntelManager

class OdinAlpha:
    def __init__(self):
        self.target = os.getenv("ASGARD_TARGET", "example.com").replace("http://", "").replace("https://", "").split("/")[0]
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.results = {"subdomains": [], "github_tokens": []}

    def enumerate_subdomains(self):
        url = f"https://crt.sh/?q=%25.{self.target}&output=json"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            subs = set()
            for entry in data:
                name = entry.get("name_value", "")
                for line in name.split("\n"):
                    if self.target in line:
                        subs.add(line.strip())
            self.results["subdomains"] = list(subs)
            self.intel.add("odin", "subdomains", len(subs))
        except:
            pass

    def search_github_tokens(self):
        gh_url = f"https://github.com/search?q={self.target}+token&type=code"
        try:
            r = requests.get(gh_url, timeout=10)
            if "token" in r.text:
                self.results["github_tokens"].append(gh_url)
                self.intel.add("odin", "github_token_leak", True)
        except:
            pass

    def save(self):
        os.makedirs(self.report_dir, exist_ok=True)
        with open(os.path.join(self.report_dir, "odin_alpha_results.json"), "w") as f:
            json.dump(self.results, f, indent=2)

    def run(self):
        print(f"[+] Odin Alpha scanning OSINT for {self.target}")
        self.enumerate_subdomains()
        self.search_github_tokens()
        self.save()
        print("[+] Odin Alpha complete.")

if __name__ == "__main__":
    OdinAlpha().run()
