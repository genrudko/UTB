# experiments/m0 — UTB-M0 environment probe artifacts

Purpose: evidence of the execution-sandbox environment for UTB-M0 (ChatGPT history
capture feasibility spike). These probes established why live provider tests A–J
could not run in this workspace.

**Security:** all probes are secret-free. They print environment variable **names**
(never values), file/directory **existence** (never contents), binary presence, and
DNS/TCP reachability results. No credentials, cookies, tokens, `cf_clearance`,
browser profiles, or chat content are read or printed.

Files:

- `probe_env.py` — platform, browser binaries, profile dirs, env var names (auth-pattern filter),
  DNS/TCP reachability, disk, git remote names.
- `probe_env2.py` — hosts/resolv presence, pip config, HTTPS reachability (pypi/github/chatgpt),
  installed distributions, local search for ChatGPT client code, `git ls-remote` offline check.
- `probe_env3.py` — full env var name list, helper CLIs, ssh config presence, mounts,
  home-dir search for vps/wake/bind/utb/mcp/chrome, /proc checks.
- `probe_env4.py` — docker daemon, routing table, egress-proxy scan.

Key measured facts (see `docs/research/UTB-M0-EVIDENCE.md` for the full report):

- DNS resolution fails for all hosts (`chatgpt.com`, `chat.openai.com`, `github.com`, `pypi.org`, …).
- No browser binary or browser profile exists.
- No auth/cookie/token environment variables exist.
- No `~/.ssh`, no Docker daemon, no mounts, no reachable egress proxy.

Re-run on the real VPS runtime if the blocker is to be re-validated.

Run: `python3 experiments/m0/probe_env.py` (and `probe_env2.py`/`probe_env3.py`/`probe_env4.py`).