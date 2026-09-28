#!/usr/bin/env python3
"""UTB-M0 environment probe (throwaway, secret-free).

Prints only environment variable NAMES and presence of infrastructure.
Never prints variable values. Never reads cookie/token files.
"""
import os
import platform
import shutil
import socket
import sys
from pathlib import Path

print("=== python ===")
print("platform:", platform.platform())
print("python:", sys.version.split()[0])

print("\n=== browser binaries (shutil.which) ===")
for name in (
    "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
    "brave-browser", "firefox", "chromedriver", "playwright",
):
    print(f"{name}: {shutil.which(name)}")

print("\n=== likely browser profile dirs (existence only) ===")
candidates = [
    Path.home() / ".config" / "google-chrome",
    Path.home() / ".config" / "chromium",
    Path.home() / ".config" / "BraveSoftware" / "Brave-Browser",
    Path.home() / ".config" / "microsoft-edge",
    Path.home() / ".cache" / "ms-playwright",
    Path.home() / ".playwright",
    Path.home() / ".wake",
    Path("/root/.config/google-chrome"),
    Path("/root/.config/chromium"),
    Path("/root/.cache/ms-playwright"),
    Path("/tmp/utb_m0"),
]
for p in candidates:
    print(f"{p}: exists={p.exists()} is_dir={p.is_dir() if p.exists() else False}")

print("\n=== env var NAMES matching auth/chatgpt/cf/proxy/token (names only) ===")
hits = sorted(
    n for n in os.environ
    if any(k in n.lower() for k in (
        "openai", "chatgpt", "cf_", "cloudflare", "token", "cookie",
        "session", "auth", "proxy", "vps", "bridge", "key", "secret",
    ))
)
print(hits if hits else "(none)")

print("\n=== network reachability (DNS + TCP only, no TLS handshake, no secrets) ===")
for host, port in (
    ("chatgpt.com", 443),
    ("chat.openai.com", 443),
    ("api.openai.com", 443),
    ("ab.chatgpt.com", 443),  # analytics endpoint used by some clients
    ("raw.githubusercontent.com", 443),
):
    try:
        ip = socket.gethostbyname(host)
        s = socket.create_connection((host, port), timeout=5)
        s.close()
        print(f"{host}:{port} reachable (ip={ip})")
    except Exception as e:  # noqa: BLE001
        print(f"{host}:{port} FAIL {type(e).__name__}: {e}")

print("\n=== storage ===")
try:
    st = shutil.disk_usage("/")
    print(f"disk total={st.total/(1<<30):.1f}GiB used={st.used/(1<<30):.1f}GiB free={st.free/(1<<30):.1f}GiB")
except Exception as e:  # noqa: BLE001
    print("disk_usage failed:", e)

print("\n=== git remotes (names only, URLs redacted) ===")
try:
    import subprocess
    out = subprocess.run(
        ["git", "remote", "-v"], capture_output=True, text=True, timeout=10
    )
    for line in out.stdout.strip().splitlines():
        name = line.split()[0] if line.split() else "?"
        print(f"remote name: {name}")
except Exception as e:  # noqa: BLE001
    print("git remote failed:", e)