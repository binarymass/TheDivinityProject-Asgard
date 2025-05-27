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
import matplotlib.pyplot as plt
from fpdf import FPDF
from yggdrasil.intel_manager import IntelManager
from transformers import pipeline

class NornsAlpha:
    def __init__(self):
        self.report_dir = os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.intel = IntelManager(self.report_dir)
        self.reports = {}
        self.model = pipeline("text-generation", model="openai-community/gpt2")
        self.pdf_path = os.path.join(self.report_dir, "norns_alpha_report.pdf")

    def collect_reports(self):
        for file in os.listdir(self.report_dir):
            if file.endswith("_results.json"):
                with open(os.path.join(self.report_dir, file), "r") as f:
                    try:
                        self.reports[file] = json.load(f)
                    except:
                        continue

    def summarize_findings(self):
        vuln_summary = []
        for module, findings in self.reports.items():
            if isinstance(findings, dict):
                for k, v in findings.items():
                    vuln_summary.append(f"{module}: {k} => {str(v)}")
        text = "Summarize this security scan with risks: " + "; ".join(vuln_summary)
        result = self.model(text, max_length=150)[0]['generated_text']
        return result.strip()

    def build_chart(self):
        vuln_counts = {}
        for mod, data in self.reports.items():
            for k in data:
                vuln_counts[k] = vuln_counts.get(k, 0) + 1
        plt.figure(figsize=(8, 4))
        plt.bar(vuln_counts.keys(), vuln_counts.values())
        plt.title("Vulnerability Summary")
        plt.ylabel("Count")
        chart_path = os.path.join(self.report_dir, "norns_chart.png")
        plt.tight_layout()
        plt.savefig(chart_path)
        return chart_path

    def create_pdf(self, summary_text, chart_img):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Asgard Norns Alpha Report", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, summary_text)
        pdf.image(chart_img, x=10, w=180)
        pdf.output(self.pdf_path)

    def run(self):
        print("[+] Norns Alpha generating report...")
        self.collect_reports()
        summary = self.summarize_findings()
        chart = self.build_chart()
        self.create_pdf(summary, chart)
        print(f"[+] Norns Alpha complete. Report saved to {self.pdf_path}")

if __name__ == "__main__":
    NornsAlpha().run()
