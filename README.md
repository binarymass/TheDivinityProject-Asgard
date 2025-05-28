
# 🛡️ Asgard Framework

The **Asgard Framework** is a modular, AI-assisted offensive security and red teaming toolkit built for full-spectrum reconnaissance, vulnerability discovery, exploitation, and reporting. Designed for professionals and researchers, it enables rapid, intelligent assessments across web, cloud, OSINT, and internal systems.

---

## ✨ Key Features

- 🔍 **10 Full Alpha Modules** covering all major phases of attack simulation:
  - **Freya** – Full-spectrum web vulnerability scanner (XSS, SQLi, RCE, SSRF, etc.)
  - **Thor** – Network recon using Nmap
  - **Odin** – OSINT and metadata intelligence
  - **Njord** – Cloud and token leakage analysis
  - **Hel** – .onion scraping over Tor
  - **Baldur** – CVE & RCE discovery
  - **Loki** – Post-exploitation and persistence
  - **Heimdall** – WAF and blacklist detection
  - **Mimir** – Intel correlation and attack path scoring
  - **Norns** – Reporting (PDF, AI summaries)

- 🤖 **AI-Enhanced**
  - Natural language REPL agent interface
  - GPT-based summary generation
  - CVSS-style scoring and intel correlation

- 🧩 **Modular Design**
  - Plugin support
  - TTP simulation
  - Stealth tools (jitter, header spoofing, Tor routing)

- 📄 **Exportable Reports**
  - PDF report generation with charts and executive summaries

- 🐳 **Docker-Ready + Installer**
  - Works in Docker or directly via shell installer
  - CI/CD integration ready

---

## 🚀 Getting Started

### Install (Linux)
```bash
chmod +x install.sh
./install.sh
```

### Run all modules
```bash
python3 yggdrasil/yggdrasil_alpha.py
```

### Enter AI agent shell
```bash
python3 yggdrasil/yggdrasil_agent.py
```

### Run a module manually
```bash
ASGARD_TARGET=https://example.com ASGARD_REPORTS_DIR=./reports python3 freya/freya_alpha.py
```

---

## 📦 Docker Usage
```bash
docker-compose up --build
```

To use REPL instead, include `docker-compose.override.yml`.

---

## 📁 Workspaces
Each target is run inside a workspace directory (`workspaces/clientA/`), isolating targets, reports, and intel data.

---

## 📜 License & Legal

Licensed under the MIT License with additional disclaimer.  
**This software is provided for authorized security testing, training, and research only.**

Violations of usage terms may result in legal consequences under CFAA, CMA, or international law.  
See `LICENSE.txt` for full disclaimer.

---

## 🧠 Built By
**The Divinity Project**

For questions, contributions, or collaborations — reach out or fork this project.
https://buymeacoffee.com/tdpunkn0wnable - if you feel up to it. not required 
---

## 🔖 Tags
`red-team` `pentesting` `web-vuln-scanner` `osint` `offensive-security` `ai-security` `cve-scanner` `docker` `reporting`
