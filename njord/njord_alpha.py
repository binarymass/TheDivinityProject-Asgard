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
import requests
from yggdrasil.intel_manager import IntelManager
from yggdrasil.stealth_tools import StealthTools

class NjordAlpha:
    def __init__(self):
        self.target = os.getenv("ASGARD_TARGET", "example.com").replace("http://", "").replace("https://", "").split("/")[0]
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.stealth = StealthTools()
        self.results = {"open_buckets": [], "github_leaks": []}

    def check_s3(self):
        s3_urls = [f"http://{self.target}.s3.amazonaws.com", f"https://s3.amazonaws.com/{self.target}"]
        for url in s3_urls:
            try:
                r = requests.get(url, headers=self.stealth.get_headers(), timeout=10)
                if "<ListBucketResult" in r.text:
                    self.results["open_buckets"].append(url)
                    self.intel.add("njord", "open_s3", True)
            except:
                continue

    def github_secret_check(self):
        search_url = f"https://github.com/search?q={self.target}+aws_secret&type=code"
        try:
            r = requests.get(search_url, headers=self.stealth.get_headers(), timeout=10)
            if "aws" in r.text.lower() and "secret" in r.text.lower():
                self.results["github_leaks"].append(search_url)
                self.intel.add("njord", "github_leak", True)
        except:
            pass

    def save(self):
        os.makedirs(self.report_dir, exist_ok=True)
        with open(os.path.join(self.report_dir, "njord_alpha_results.json"), "w") as f:
            json.dump(self.results, f, indent=2)

    def run(self):
        print(f"[+] Njord Alpha cloud scan for {self.target}")
        self.check_s3()
        self.github_secret_check()
        self.save()
        print("[+] Njord Alpha complete.")

if __name__ == "__main__":
    NjordAlpha().run()
