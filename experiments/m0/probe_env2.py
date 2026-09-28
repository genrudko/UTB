#!/usr/bin/env python3
"""UTB-M0 second environment probe (throwaway, secret-free).

Confirms network isolation, checks local caches/installed packages/logical
locations for reusable ChatGPT client/export code. Prints names only.
"""
import importlib.metadata
import os
import shutil
import socket
import subprocess
from pathlib import Path

print("=== /etc/hosts (non-comment lines) ===")
try:
    for line in Path("/etc/hosts").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            print(line)
except Exception as e:  # noqa: BLE001
    print("hosts read failed:", e)

print("\n=== /etc/resolv.conf (redacted: only nameserver IP presence) ===")
try:
    for line in Path("/etc/resolv.conf").read_text().splitlines():
        line = line.strip()
        if line.startswith("nameserver"):
            print("nameserver: <present>")
        elif line.startswith("search") or line.startswith("domain"):
            print(line.split()[0] + ": <present>")
except Exception as e:  # noqa: BLE001
    print("resolv read failed:", e)

print("\n=== pip / uv presence ===")
print("pip:", shutil.which("pip"), "pip3:", shutil.which("pip3"), "uv:", shutil.which("uv"))

print("\n=== pip config / index URLs (urls only, no credentials) ===")
for cmd in (["pip", "config", "list"], ["pip3", "config", "list"]):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        for line in out.stdout.splitlines():
            if "index-url" in line or "extra-index-url" in line:
                print(line)
    except Exception as e:  # noqa: BLE001
        print(f"{cmd[0]} config failed: {e}")

print("\n=== HTTP(S) reachability attempts (urllib, short timeout) ===")
import urllib.request  # noqa: E402

for url in (
    "https://pypi.org/simple/",
    "https://github.com/FrankCJones/chatgpt-export",
    "http://chatgpt.com/",
):
    try:
        with urllib.request.urlopen(url, timeout=6) as r:
            print(f"{url} -> HTTP {r.status}")
    except Exception as e:  # noqa: BLE001
        print(f"{url} -> {type(e).__name__}: {e}")

print("\n=== installed distributions matching chatgpt/openai/export/playwright/selenium ===")
try:
    names = sorted(d.metadata["Name"] for d in importlib.metadata.distributions())
except Exception as e:  # noqa: BLE001
    print("metadata listing failed:", e)
    names = []
interesting = [n for n in names if any(
    k in n.lower() for k in ("openai", "chatgpt", "export", "playwright", "selenium", "requests", "httpx", "cloudscraper", "undetected")
)]
print(interesting if interesting else "(none found)")
print("total distributions:", len(names))

print("\n=== local search for ChatGPT client code (bounded dirs, filenames only) ===")
roots = [Path.home(), Path("/opt"), Path("/usr/local"), Path("/workspace"), Path("/srv")]
keywords = ("backend-api", "chatgpt", "chat.openai", "conversations", "cf_clearance")
hits = []
for root in roots:
    if not root.exists():
        continue
    for base in ("chatgpt", "chatgpt-export", "aishell", "reminic", "remnic", "capture"):
        p = root / base
        if p.exists():
            hits.append(str(p))
    try:
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            if p.stat().st_size > 2_000_000:
                continue
            try:
                text = p.read_text(errors="ignore")[:4000]
            except Exception:  # noqa: BLE001
                continue
            low = text.lower()
            if any(k in low for k in keywords):
                hits.append(str(p))
                if len(hits) > 60:
                    break
    except Exception as e:  # noqa: BLE001
        print(f"rglob {root} failed: {e}")
print("\n".join(sorted(set(hits))) if hits else "(no local candidates found)")

print("\n=== git usable offline? ===")
try:
    out = subprocess.run(
        ["git", "ls-remote", "https://github.com/FrankCJones/chatgpt-export.git"],
        capture_output=True, text=True, timeout=15,
    )
    print("ls-remote exit:", out.returncode, "| stderr tail:", (out.stderr or "").strip().splitlines()[-1:] or "none")
except Exception as e:  # noqa: BLE001
    print("git ls-remote failed:", e)