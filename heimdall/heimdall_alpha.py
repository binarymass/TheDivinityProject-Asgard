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

class HeimdallAlpha:
    def __init__(self):
        self.target = os.getenv("ASGARD_TARGET", "http://localhost")
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.stealth = StealthTools()
        self.results = {"waf_detected": False, "dns_blacklisted": []}

    def check_waf(self):
        payload = "/<script>alert(1)</script>"
        try:
            r = requests.get(self.target + payload, headers=self.stealth.get_headers(), timeout=10)
            if r.status_code in [403, 406] or "waf" in r.text.lower():
                self.results["waf_detected"] = True
                self.intel.add("heimdall", "waf", True)
        except:
            pass

    def check_dns_blacklist(self):
        dnsbls = [
            "zen.spamhaus.org",
            "bl.spamcop.net",
            "dnsbl.sorbs.net"
        ]
        ip = self.target.replace("http://", "").replace("https://", "").split("/")[0]
        try:
            import socket
            ip_addr = socket.gethostbyname(ip)
            reversed_ip = ".".join(reversed(ip_addr.split(".")))
            for bl in dnsbls:
                try:
                    socket.gethostbyname(f"{reversed_ip}.{bl}")
                    self.results["dns_blacklisted"].append(bl)
                    self.intel.add("heimdall", "dns_blacklist", True)
                except:
                    continue
        except:
            pass

    def save(self):
        os.makedirs(self.report_dir, exist_ok=True)
        with open(os.path.join(self.report_dir, "heimdall_alpha_results.json"), "w") as f:
            json.dump(self.results, f, indent=2)

    def run(self):
        print("[+] Heimdall Alpha scanning for defenses...")
        self.check_waf()
        self.check_dns_blacklist()
        self.save()
        print("[+] Heimdall Alpha complete.")

if __name__ == "__main__":
    HeimdallAlpha().run()
