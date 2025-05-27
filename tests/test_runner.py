
import os
import subprocess
import json
import time

TARGET = "https://example.com"
WORKSPACE = "./test_workspace"
REPORTS = f"{WORKSPACE}/reports"
INTEL_PATH = f"{REPORTS}/intel.json"
MODULES = [
    "thor", "odin", "freya", "baldur", "njord",
    "heimdall", "hel", "loki", "mimir", "norns"
]

def setup_environment():
    os.makedirs(REPORTS, exist_ok=True)
    os.environ["ASGARD_TARGET"] = TARGET
    os.environ["ASGARD_REPORTS_DIR"] = REPORTS
    if os.path.exists(INTEL_PATH):
        os.remove(INTEL_PATH)

def run_module(name):
    try:
        print(f"[*] Testing module: {name}")
        subprocess.run(["python3", f"{name}/{name}_alpha.py"], timeout=30)
        result_path = os.path.join(REPORTS, f"{name}_alpha_results.json")
        if os.path.exists(result_path):
            with open(result_path) as f:
                json.load(f)  # Ensure it's valid JSON
            return True
        else:
            print(f"[!] No result file for {name}")
            return False
    except Exception as e:
        print(f"[!] Exception in {name}: {e}")
        return False

def validate_intel():
    try:
        with open(INTEL_PATH) as f:
            data = json.load(f)
            return isinstance(data, dict)
    except:
        return False

def run_tests():
    setup_environment()
    results = {}
    for mod in MODULES:
        results[mod] = run_module(mod)
    intel_ok = validate_intel()
    results["intel_integrity"] = intel_ok
    with open("test_report.txt", "w") as report:
        for k, v in results.items():
            report.write(f"{k}: {'PASS' if v else 'FAIL'}\n")
    print("[*] Test run complete. Results in test_report.txt")

if __name__ == "__main__":
    run_tests()
