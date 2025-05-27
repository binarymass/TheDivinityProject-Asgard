
import os
import json
import matplotlib.pyplot as plt
from fpdf import FPDF
from transformers import pipeline

class NornsBeta:
    def __init__(self, report_dir):
        self.report_dir = report_dir
        self.model = pipeline("text-generation", model="openai-community/gpt2")
        self.summary = ""
        self.vuln_stats = {}
        self.report_data = {}

    def load_reports(self):
        for file in os.listdir(self.report_dir):
            if file.endswith(".json") and file != "intel.json":
                path = os.path.join(self.report_dir, file)
                try:
                    with open(path, "r") as f:
                        self.report_data[file] = json.load(f)
                except:
                    continue

    def analyze_vulnerabilities(self):
        counts = {"rce": 0, "sqli": 0, "xss": 0, "ssti": 0}
        for content in self.report_data.values():
            if isinstance(content, dict):
                for k in counts.keys():
                    if k in content:
                        counts[k] += len(content.get(k, []))
        self.vuln_stats = counts

    def generate_ai_summary(self):
        vuln_context = ", ".join([f"{k.upper()}={v}" for k, v in self.vuln_stats.items()])
        prompt = f"Summarize risk level and findings for a test that found: {vuln_context}"
        result = self.model(prompt, max_length=100)[0]['generated_text']
        self.summary = result.strip()

    def build_charts(self):
        plt.figure(figsize=(6, 4))
        names = list(self.vuln_stats.keys())
        values = list(self.vuln_stats.values())
        plt.bar(names, values)
        plt.title("Vulnerability Type Counts")
        plt.ylabel("Occurrences")
        plt.tight_layout()
        chart_path = os.path.join(self.report_dir, "vuln_chart.png")
        plt.savefig(chart_path)
        return chart_path

    def export_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Asgard Norns Report", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, self.summary)
        chart = self.build_charts()
        pdf.image(chart, x=10, y=None, w=180)
        pdf_path = os.path.join(self.report_dir, "norns_beta_final_report.pdf")
        pdf.output(pdf_path)
        return pdf_path

    def run(self):
        self.load_reports()
        self.analyze_vulnerabilities()
        self.generate_ai_summary()
        self.export_pdf()
