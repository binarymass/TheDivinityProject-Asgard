
import os
import subprocess
from transformers import pipeline
from yggdrasil.workspace_manager import WorkspaceManager
from yggdrasil.intel_manager import IntelManager

class YggdrasilAgent:
    def __init__(self):
        self.ws = WorkspaceManager()
        self.ws.load_active_workspace()
        self.target = os.getenv("ASGARD_TARGET", "default")
        self.intel = IntelManager(self.ws.get_path("reports"))
        self.model = pipeline("text-generation", model="openai-community/gpt2")
        print(f"[+] Loaded workspace: {self.ws.active}")
        print(f"[+] Target context: {self.target}")

    def parse_command(self, text):
        text = text.lower()
        if "freya" in text or "web" in text or "form" in text:
            return "freya"
        elif "recon" in text or "scan" in text or "port" in text:
            return "thor"
        elif "osint" in text or "leak" in text or "profile" in text:
            return "odin"
        elif "cloud" in text or "s3" in text or "azure" in text:
            return "njord"
        elif "rce" in text or "exploit" in text:
            return "baldur"
        elif "persist" in text or "post" in text:
            return "loki"
        elif "defense" in text or "waf" in text:
            return "heimdall"
        elif "darknet" in text or "tor" in text or "onion" in text:
            return "hel"
        elif "correlate" in text or "score" in text or "intel" in text:
            return "mimir"
        elif "report" in text or "summary" in text:
            return "norns"
        elif "full chain" in text or "everything" in text:
            return "chain"
        return None

    def run(self):
        while True:
            cmd = input("asgard> ").strip()
            if cmd in ["exit", "quit"]:
                print("[*] Exiting agent.")
                break

            module = self.parse_command(cmd)
            if not module:
                print("[!] I don't understand that command.")
                continue

            if module == "chain":
                self.run_chain()
            else:
                self.run_module(module)

    def run_module(self, name):
        print(f"[+] Executing module: {name}")
        os.environ["ASGARD_REPORTS_DIR"] = self.ws.get_path("reports") or "./reports"
        os.environ["ASGARD_TARGET"] = self.target
        subprocess.run(["python3", f"{name}/{name}_alpha.py"])

    def run_chain(self):
        for name in ["thor", "odin", "freya", "baldur", "njord", "heimdall", "hel", "loki", "mimir", "norns"]:
            self.run_module(name)

if __name__ == "__main__":
    YggdrasilAgent().run()
