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

class HelAlpha:
    def __init__(self):
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.keywords = ["password", "login", "access", "exploit", "credential"]
        self.targets = [
            "http://3g2upl4pq6kufc4m.onion",  # DuckDuckGo
            "http://zlal32teyptf4tvi.onion",  # Sci-Hub mirror (example only)
        ]
        self.results = {}

    def search_onion_sites(self):
        for site in self.targets:
            try:
                r = self.session.get(site, timeout=20)
                hits = [k for k in self.keywords if k in r.text.lower()]
                if hits:
                    self.results[site] = hits
                    self.intel.add("hel", site, hits)
            except:
                continue

    def save(self):
        os.makedirs(self.report_dir, exist_ok=True)
        with open(os.path.join(self.report_dir, "hel_alpha_results.json"), "w") as f:
            json.dump(self.results, f, indent=2)

    def run(self):
        print("[+] Hel Alpha crawling onion sites via Tor...")
        self.search_onion_sites()
        self.save()
        print("[+] Hel Alpha complete.")

if __name__ == "__main__":
    HelAlpha().run()
