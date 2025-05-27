
import os
import datetime

class TeamTools:
    def __init__(self, report_dir=None, operator_name="anonymous"):
        self.report_dir = report_dir or os.getenv("ASGARD_REPORTS_DIR", "./reports")
        self.operator = operator_name
        self.audit_file = os.path.join(self.report_dir, "audit.log")
        self.notes_file = os.path.join(self.report_dir, "team_notes.md")

    def log_action(self, module_name, target=None, action="executed"):
        timestamp = datetime.datetime.now().isoformat()
        entry = f"[{timestamp}] {self.operator} {action} {module_name}"
        if target:
            entry += f" on {target}"
        with open(self.audit_file, "a") as f:
            f.write(entry + "\n")

    def add_note(self, note):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(self.notes_file, "a") as f:
            f.write(f"### {timestamp} — {self.operator}\n{note}\n\n")
