
# 🧾 Asgard Framework – Full Documentation

---

## 🔹 Overview

The **Asgard Framework** is a modular, open-source, AI-assisted offensive security and red teaming toolkit. It combines classic penetration testing workflows with automated intelligence gathering, exploitation, reporting, and chaining across multiple phases of simulated attacks.

Developed by **The Divinity Project**, Asgard is distributed under the MIT license with a strong emphasis on lawful use, research, and education.

---

## 📁 Module Overview

### 1. Freya – Web Application Scanner
- Detects: XSS, SQLi, SSRF, IDOR, CRLF, SSTI, RCE, Path Traversal, XXE, Open Redirect, WebSocket, CSRF, Host Header Injection, OAuth misconfigurations, Authentication bypass
- JSON output + AI-enhanced CVSS summaries
- Integrates with Norns for report generation

### 2. Thor – Recon & Scanning
- Full-range Nmap scanner
- Header spoofing, rate controls, stealth options
- Scans passed to Baldur for CVE correlation

### 3. Odin – OSINT & Metadata
- WHOIS, subdomain bruteforce, email & social lookup
- GitHub leak checks, Shodan, and metadata from images
- All data written to `intel.json`

### 4. Njord – Cloud & Token Exposure
- Scans S3 buckets, public cloud assets
- GitHub token search via API
- DNS takeover detection and reporting

### 5. Baldur – Exploit Discovery
- Pulls CVEs from online databases (e.g. Exploit-DB, NVD)
- Matches CVEs to software detected by Thor
- Exploit proof-of-concept test and results

### 6. Hel – Darknet/Onion Search
- Tor crawler with .onion search capabilities
- Keyword-based intelligence collection
- Fully contained over SOCKS5

### 7. Heimdall – WAF & Defense Detection
- Probes for CDN, firewall, rate-limiting behavior
- Blacklist checks for known IP reputation
- Flags WAF fingerprints via headers and behavior

### 8. Loki – Post-Exploitation
- Supports cron jobs, Windows tasks, basic backdoors
- Integrates with SET (Social Engineer Toolkit)
- AI-suggested persistence logic

### 9. Mimir – Correlation & Scoring
- Aggregates intel from all modules
- Scores risks CVSS-style
- Prepares data for final report

### 10. Norns – Reporting Engine
- Creates `.pdf` reports w/:
  - CVSS scoring
  - Graphs
  - AI summaries
  - Recommendations
- Compiles `intel.json` data into final documents

---

## 🧠 AI Integration

### Used In:
- REPL Agent (Yggdrasil)
- Report writing (Norns)
- Exploit crafting (Baldur)
- Chain simulation (Mimir)

To enable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

---

## 🔧 Running Modules

Each module accepts target from environment:
```bash
export ASGARD_TARGET=https://example.com
export ASGARD_REPORTS_DIR=./reports/example
python3 freya/freya_alpha.py
```

---

## 🤖 Yggdrasil – Main Controller

### Alpha Mode:
```bash
python3 yggdrasil/yggdrasil_alpha.py
```

### AI Agent Mode:
```bash
python3 yggdrasil/yggdrasil_agent.py
```

### Available Agent Commands:
- `scan for open ports`
- `run full web scan`
- `generate report`
- `fetch recent exploits`

---

## 🧩 Plugins

Drop plugins into `/plugins` with:
```python
def run_plugin(target, config):
    ...
```

They will be automatically detected and can be called via agent.

---

## 🧪 Testing Setup

Run tests in `/tests`:
```bash
python3 tests/module_test_suite.py
```

---

## 🐳 Docker Usage

```bash
docker-compose up --build
```

Docker will auto-run Yggdrasil in AI agent mode if `OPENAI_API_KEY` is passed.

---

## 📄 Reporting

Output files:
- `*.json` per module
- `intel.json` – Unified data
- `report.pdf` – Final deliverable

---

## 🔐 Legal

Asgard is for:
- Licensed red teams
- Security researchers
- Educators
- CTFs

**Not for unauthorized use.**

---

## 🔖 Resources

- Repo: https://github.com/binarymass/TheDivinityProject-Asgard
- License: MIT + extended liability disclaimer
- Docs: (This file)
- Manual: `Asgard_User_Manual.md`
- Contact: The Divinity Project via GitHub

---

## 💬 Final Note

Asgard is an evolving platform. You are encouraged to fork, contribute, and report issues. Use responsibly.

