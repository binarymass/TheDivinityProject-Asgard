
#!/bin/bash
echo "[+] Initializing Asgard..."
mkdir -p workspaces/default
echo "https://example.com" > workspaces/default/targets.txt
echo "[+] Launching..."
python3 yggdrasil/yggdrasil_alpha.py
