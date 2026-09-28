#!/usr/bin/env python3
"""UTB-M0 third probe: any remote-access affordance (secret-free, names only)."""
import os
import shutil
import subprocess
from pathlib import Path

print("=== full env var NAMES ===")
print(sorted(os.environ.keys()))

print("\n=== helper CLIs ===")
for name in ("gh", "codex", "ssh", "scp", "sftp", "curl", "wget", "chromium", "docker", "podman", "node", "npm"):
    print(f"{name}: {shutil.which(name)}")

print("\n=== ssh config presence (no contents, no keys) ===")
ssh = Path.home() / ".ssh"
print(f"{ssh}: exists={ssh.exists()}")
if ssh.exists():
    for p in sorted(ssh.iterdir()):
        print("  entry:", p.name, "is_dir=", p.is_dir())
print("known_hosts exists:", (ssh / "known_hosts").exists())

print("\n=== mounts ===")
try:
    out = subprocess.run(["cat", "/proc/mounts"], capture_output=True, text=True, timeout=10)
    for line in out.stdout.splitlines()[:60]:
        parts = line.split()
        if parts and (parts[0].startswith("/") or "overlay" in parts[0] or "tmpfs" in parts[0]):
            print(parts[0], "->", parts[1])
except Exception as e:  # noqa: BLE001
    print("mounts failed:", e)

print("\n=== search home for vps/wake/bind/utb references (filenames only) ===")
roots = [Path.home()]
hits = []
for root in roots:
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        low = p.name.lower()
        if any(k in low for k in ("vps", "wake", "bind", "utb", "mcp", "chrome")):
            hits.append(str(p))
print("\n".join(sorted(set(hits))) if hits else "(none)")

print("\n=== /proc/1 cmdline ===")
try:
    out = subprocess.run(["tr", "\\0", " "], stdin=open("/proc/1/cmdline"), capture_output=True, text=True, timeout=10)
    print(out.stdout.strip()[:500])
except Exception as e:  # noqa: BLE001
    print("proc/1 failed:", e)