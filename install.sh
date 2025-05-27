
#!/bin/bash

echo "[*] Asgard Framework Installer"
echo "[*] Creating Python environment..."
python3 -m venv asgard_env
source asgard_env/bin/activate

echo "[*] Installing requirements..."
pip install --upgrade pip
pip install transformers requests beautifulsoup4 matplotlib fpdf

echo "[*] Creating workspace structure..."
mkdir -p workspaces/default/reports
echo "https://example.com" > workspaces/default/targets.txt

echo "[*] Asgard Framework installed."
echo "[*] To run full chain: source asgard_env/bin/activate && python3 yggdrasil/yggdrasil_alpha.py"
echo "[*] To enter interactive REPL: python3 yggdrasil/yggdrasil_agent.py"
