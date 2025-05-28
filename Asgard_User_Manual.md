
# 📘 Asgard Framework – User Manual & Instruction Guide

Welcome to the **Asgard Framework**, a modular, AI-assisted toolkit for offensive security, penetration testing, OSINT collection, and automated reporting.

---

## 🛠️ Requirements

- Python 3.8+
- pip
- Recommended: Linux or WSL
- Optional: Docker & Docker Compose
- Optional: OpenAI API Key (for AI-assisted features)

---

## 🔧 Installation

### Option 1: Native Install
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Docker
```bash
docker-compose up --build
```

---

## 🧭 Getting Started

### Step 1 – Configure Your Environment
Set environment variables before running a module:
```bash
export ASGARD_TARGET=https://example.com
export ASGARD_REPORTS_DIR=./reports
```

### Step 2 – Run A Module
```bash
python3 freya/freya_alpha.py
```

### Step 3 – Use the Central Controller
Launch the Asgard framework from the central hub:
```bash
python3 yggdrasil/yggdrasil_alpha.py
```

### Step 4 – Use the AI Agent Shell
```bash
python3 yggdrasil/yggdrasil_agent.py
```
Try typing: `scan for web vulnerabilities` or `recon target`

---

## 📂 Directory Structure

```
/freya        - Web scanner
/thor         - Network recon (Nmap)
/odin         - OSINT & metadata
/njord        - Cloud exposure
/baldur       - CVE & exploit testing
/loki         - Post-exploitation
/heimdall     - WAF/detection
/hel          - Tor crawler
/mimir        - Scoring & correlation
/norns        - Reporting module
/yggdrasil    - Main controller & agent
/plugins      - Custom modules
/workspaces   - Target folders
```

---

## 📈 Reporting

All findings are saved as:
- `intel.json` – Raw correlated results
- `*.json` – Per-module logs
- `report.pdf` – Finalized output from Norns

---

## 🔐 AI Integration

To enable GPT-based features:
```bash
export OPENAI_API_KEY=your_api_key_here
```

Used in:
- AI summaries (Norns)
- Natural language control (Yggdrasil agent)
- Risk scoring (Mimir)

---

## 🧩 Plugins

Add Python scripts to `/plugins/`. Use this structure:
```python
def run_plugin(target, config):
    # Your code here
```

They will auto-load and be available via Yggdrasil.

---

## 🧪 Test A Target (Example)

```bash
ASGARD_TARGET=https://testphp.vulnweb.com ASGARD_REPORTS_DIR=./reports/test1 python3 freya/freya_alpha.py
```

Then:
```bash
python3 norns/norns_alpha.py
```

---

## ⚠️ Legal Disclaimer

This software is provided under the MIT license for:
- Authorized testing
- Research
- Education

**Unauthorized use against systems you don’t own or have permission to test is illegal.**

---

## 📫 Support

GitHub: [https://github.com/binarymass/TheDivinityProject-Asgard](https://github.com/binarymass/TheDivinityProject-Asgard)  
Built by: **The Divinity Project**

---

Happy hacking.
