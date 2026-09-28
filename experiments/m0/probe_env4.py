#!/usr/bin/env python3
"""UTB-M0 fourth probe: docker images, routing/gateway, possible egress proxy.
Secret-free; names only; no credential material.
"""
import socket
import subprocess
from pathlib import Path

print("=== docker images (names/tags/sizes only) ===")
try:
    out = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}} {{.Size}}"],
                         capture_output=True, text=True, timeout=20)
    print("exit:", out.returncode)
    print(out.stdout.strip() or "(no images)")
    if out.stderr.strip():
        print("stderr:", out.stderr.strip().splitlines()[-2:])
except Exception as e:  # noqa: BLE001
    print("docker failed:", e)

print("\n=== routing table ===")
for path in ("/proc/net/route", "/proc/net/if_inet6"):
    try:
        data = Path(path).read_text()
        print(f"--- {path} ---")
        print(data[:2000])
    except Exception as e:  # noqa: BLE001
        print(f"{path}: {e}")

print("\n=== try common egress proxy ports on gateway (TCP only) ===")
try:
    # parse default gateway from /proc/net/route (first line after header with 0.0.0.0 dest)
    gw = None
    for line in Path("/proc/net/route").read_text().splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "00000000":
            gw = socket.inet_ntoa(int(parts[2], 16).to_bytes(4, "little"))
            break
    print("gateway:", gw)
    if gw:
        for port in (3128, 8080, 8888, 8000, 1080, 10809):
            try:
                s = socket.create_connection((gw, port), timeout=3)
                s.close()
                print(f"  gateway:{port} OPEN")
            except Exception:  # noqa: BLE001
                pass
except Exception as e:  # noqa: BLE001
    print("routing/proxy probe failed:", e)