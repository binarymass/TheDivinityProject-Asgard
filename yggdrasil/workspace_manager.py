
import os
import json

class WorkspaceManager:
    def __init__(self, base_dir="./workspaces"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.active = None

    def list_workspaces(self):
        return [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]

    def create_workspace(self, name):
        path = os.path.join(self.base_dir, name)
        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, "config"), exist_ok=True)
        os.makedirs(os.path.join(path, "reports"), exist_ok=True)
        self.set_active_workspace(name)

    def set_active_workspace(self, name):
        self.active = os.path.join(self.base_dir, name)
        with open("current_workspace.txt", "w") as f:
            f.write(self.active)

    def load_active_workspace(self):
        if os.path.exists("current_workspace.txt"):
            with open("current_workspace.txt", "r") as f:
                self.active = f.read().strip()
        return self.active

    def get_path(self, subdir):
        if self.active:
            return os.path.join(self.active, subdir)
        return None
