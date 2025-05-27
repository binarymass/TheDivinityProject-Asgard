
@echo off
echo [*] Initializing Asgard...
mkdir workspaces\default
echo https://example.com > workspaces\default\targets.txt
echo [*] Launching...
python yggdrasil\yggdrasil_alpha.py
