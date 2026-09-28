# UTB-M0 — Evidence Report: ChatGPT History Capture Feasibility

**Stage:** UTB-M0 (bounded research spike)
**Status:** **BLOCKED — environment blocker (no network / no browser / no authenticated profile in execution sandbox)**
**Branch:** `research/utb-m0-chat-history-capture`
**Repository base commit:** `516b3f8`
**Report date:** spike execution date
**Owner:** M0 executor (report returned to Canonical Architect per contract §10)

> Honesty rule applied throughout: **no live provider test A–J was executed**, therefore
> **no PASS/PARTIAL/FAIL value is claimed**. This report records the blocker with exact
> measured environment facts so the coordinator can re-run M0 in a networked VPS runtime.
> Nothing here is fabricated; provider-touching rows are marked BLOCKED/UNMEASURED.

---

## 1. Test environment (measured — FACT)

Measured inside the execution sandbox that was provided for this M0 run (`/tmp/sandbox-home`).

| Item | Measured value (FACT) |
|---|---|
| OS / platform | Linux 6.8.0-138-generic x86_64 glibc 2.39 |
| Python | 3.12.3 |
| Environment variables | only `HOME`, `LANG`, `PATH`, `PWD` are set (names listed; no auth/proxy/OPENAI/CHATGPT/CF/TOKEN/COOKIE/SESSION variables exist) |
| Browser binaries | none present: `chromium`, `chromium-browser`, `google-chrome`, `google-chrome-stable`, `brave-browser`, `firefox`, `chromedriver`, `playwright` all absent (`shutil.which` → None) |
| Browser profiles | none present: `~/.config/google-chrome`, `~/.config/chromium`, `~/.config/BraveSoftware/Brave-Browser`, `~/.config/microsoft-edge`, `~/.cache/ms-playwright`, `~/.playwright`, `~/.wake`, `/root/.config/*`, `/tmp/utb_m0` all non-existent |
| Network / DNS | `chatgpt.com:443`, `chat.openai.com:443`, `api.openai.com:443`, `ab.chatgpt.com:443`, `raw.githubusercontent.com:443`, `github.com` (git ls-remote), `pypi.org` (HTTPS) all fail with `gaierror: Temporary failure in name resolution`. No `/etc/hosts`, no `/etc/resolv.conf`, no `/proc/net/*` in sandbox → no DNS and no route table |
| Egress proxies | no proxy env vars; no reachable gateway/proxy ports found (no route table to scan) |
| Remote access | no `~/.ssh` directory, no `known_hosts`, no Docker daemon (`/var/run/docker.sock` absent), no mounts |
| Installed Python libs (relevant) | `requests`, `httpx2` present; **no** `openai`, `playwright`, `selenium`, `cloudscraper`, exporter packages |
| Local ChatGPT client code | none found in `$HOME`, `/opt`, `/usr/local`, `/workspace`, `/srv` (only `@openai/codex` README files, which are not history exporters) |
| Storage | 3.9 GiB total, 0.0 GiB used at probe time |
| Git | branch `research/utb-m0-chat-history-capture` tracking `origin/...`, working tree clean at start, base commit `516b3f8` |

**Conclusion (FACT):** the A–J live tests require (a) network egress to `chatgpt.com`/`chat.openai.com`, and (b) the VPS authenticated Chromium profile (per contract §4 assumptions). Neither exists in this sandbox. **INFERENCE:** the sandbox is an offline repository-execution workspace, not the VPS runtime the contract assumes; live M0 cannot be performed here.

---

## 2. Exact sequence actually performed

1. Read authoritative files in full (`README.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`, `docs/DECISIONS.md`, `docs/tasks/UTB-M0-chat-history-capture-spike.md`).
2. Confirmed `AGENTS.md` does not exist in the repository (searched - none; governing docs are the canonical set above).
3. Confirmed git state: branch `research/utb-m0-chat-history-capture`, clean tree, base `516b3f8`.
4. Ran **probe_env.py** (secret-free) — see §1 measured facts: platform, browser binaries (none), profile dirs (none), env var names (none matching auth patterns), DNS/TCP reachability (all fail), disk, git remotes (names only).
5. Ran **probe_env2.py** — confirmed no `/etc/hosts` / `/etc/resolv.conf`, pip index absent, HTTPS to pypi/github/chatgpt fails, no relevant installed packages, no local ChatGPT exporter code, `git ls-remote` to upstream fails with DNS error.
6. Ran **probe_env3.py** — full env var name list, helper CLIs present (`gh`, `codex`, `ssh`, `scp`, `sftp`, `curl`, `wget`, `docker`, `node`, `npm`), no `~/.ssh`, no known_hosts, no mounts, no local vps/wake/bind/utb/mcp/chrome files.
7. Ran **probe_env4.py** — Docker daemon absent, no `/proc/net/route`, no reachable egress proxy on gateway (no route table), confirming hard network isolation.
8. Per contract §10 stop condition (“Stop on an … environment blocker”) and the rule “if … cannot be handled by normal … retry/backoff, record evidence and stop that path”, **stopped the live provider path** after verifying the blocker is environmental and not resolvable by auth refresh/retry.
9. Produced this evidence report, the reuse inventory, and the capture-options comparison using only honestly-labeled material (nothing measured → nothing claimed measured).
10. Confirmed git status contains only M0-scoped changes and committed deliverables/probe artifacts on `research/utb-m0-chat-history-capture` (see commit SHA in §7).

**Environment probe artifacts** (secret-free, run above): `experiments/m0/probe_env.py`, `experiments/m0/probe_env2.py`, `experiments/m0/probe_env3.py`, `experiments/m0/probe_env4.py`.

---

## 3. Test-by-test status (A–J)

Each row states the intended contract procedure and the actual outcome in this workspace. **No row contains a fabricated measurement.**

### Test A — Baseline account-wide listing
- **Intended:** obtain recent conversation list from VPS authenticated context via least-invasive reusable method; record transport/endpoint class, response shape, IDs/timestamps, request counts/statuses, whether Chromium must stay running.
- **Actual:** BLOCKED. No network egress to `chatgpt.com`; no authenticated context exists in sandbox (no profile, no cookies/tokens, no env auth). No request was sent.
- **Evidence recorded:** environment blocker facts in §1.

### Test B — Android-only update
- **Intended:** disposable conversation updated only on Android, never opened in Web before VPS probe, discovered via account-wide mechanism; history fetched to prove the Android turn is present.
- **Actual:** BLOCKED. Requires user/owner interaction with the real Android account and a functioning VPS history path. Neither possible here.
- Per contract (“Do not claim PASS unless provenance … is actually supportable”): no provenance was established; no claim made.

### Test C — Parallel conversations (4–5)
- **Intended:** update 4–5 disposable/low-risk chats closely together; confirm one account-wide discovery pass distinguishes them without tab-per-chat and without turn mixing.
- **Actual:** BLOCKED (no network/account path).

### Test D — Branch/edit/version representation
- **Intended:** disposable chat with explicit branch/edit; record conversation/message IDs, parent/child/version fields, active-branch representation, old-branch retrievability.
- **Actual:** BLOCKED. No provider responses to inspect; no assumption from old API docs is recorded as fact.

### Test E — Project conversation representation
- **Intended:** disposable chat inside a ChatGPT Project; record how project membership/discovery appear in current responses.
- **Actual:** BLOCKED (no provider path).

### Test F — Long conversation retrieval
- **Intended:** one sufficiently long disposable/safe conversation; determine full tree vs limited turns vs pagination vs current-path, without bulk-downloading sensitive history.
- **Actual:** BLOCKED (no provider path).

### Test G — Browser-close → HTTP lifetime
- **Intended:** refresh/bootstrap auth with existing VPS Chromium profile; close Chromium fully; continue read-only HTTP probes; report observed duration / lower bound only.
- **Actual:** BLOCKED. No Chromium binary or profile exists in sandbox. No lower bound can be reported; ultimate expiry unknown. **No value invented.**

### Test H — Ephemeral auth refresh
- **Intended:** if auth became unusable, launch existing profile, refresh legitimately required state, close it, retry HTTP read.
- **Actual:** NOT TRIGGERED (blocked) — auth was never usable in this workspace, so expiry/refresh could not be exercised. Marked NOT TRIGGERED for the correct reason (bootstrap impossibility), not as a pass/fail.

### Test I — Incremental/rate behaviour
- **Intended:** conservative changed-conversation discovery cadence; record request count/concurrency/statuses, Retry-After/429 if any, unchanged-skip behavior, full-body refetch requirement. No stress test.
- **Actual:** BLOCKED (no requests possible). No 429/Retry-After observation.

### Test J — MCP correlation observation
- **Intended:** timestamp VPS Chromium launches/closes, wake/bind activity, and any naturally observed ChatGPT MCP tool-exposure disappearance/recovery.
- **Actual:** insufficient evidence — no browser/profile/wake activity exists in sandbox, so no correlation can be observed or ruled in/out. Label: **insufficient evidence**, not “no correlation observed”.

---

## 4. Acceptance matrix (contract §8) — filled honestly

| Check | Result | Evidence |
|---|---|---|
| VPS conversation list | **BLOCKED** | no network egress / no auth context in exec sandbox (see §1); endpoint/transport not observable here |
| Android-only update visible | **BLOCKED** | requires real Android-only stimulus + VPS path; not exercised |
| 4–5 parallel chats | **BLOCKED** | requires provider access; not exercised |
| Branch/version semantics | **BLOCKED** | no provider responses obtained; no old-doc assumptions recorded |
| Project chat semantics | **BLOCKED** | no provider responses obtained |
| Long-chat retrieval semantics | **BLOCKED** | no provider responses obtained |
| Chromium closed → HTTP works | **BLOCKED** | no Chromium binary/profile in sandbox (`shutil.which` → None; profile dirs absent) |
| Auth lifetime | **unknown (unmeasurable here)** | no auth existed to measure; contract explicitly forbids inventing expiry |
| Ephemeral refresh | **NOT TRIGGERED (blocked)** | refresh cannot bootstrap without profile/network |
| Incremental discovery | **BLOCKED** | no requests sent |
| 429/rate behaviour | **not observed (blocked)** | zero requests; cadence/statuses unavailable |
| Browser RAM peak | **not measured** | no browser present to launch |
| Steady-state browser RAM | **not measured** | target state “browser terminated” not exercisable; no browser |
| MCP correlation | **insufficient evidence** | no Chromium/wake activity in sandbox; no MCP trace monitored |

Contract success criterion: M0 succeeds if it **reduces capture-architecture uncertainty with trustworthy evidence**.
In this workspace, the trustworthy result is: **the provided execution sandbox cannot reach the VPS/ChatGPT runtime, so none of the provider hypotheses (H-001…H-006) were exercised.** No decision-relevant provider measurement was produced, and none is implied.

---

## 5. FACT vs INFERENCE separation

**FACT (directly measured in this workspace)**
- DNS resolution fails for chatgpt.com, chat.openai.com, api.openai.com, ab.chatgpt.com, raw.githubusercontent.com, github.com, pypi.org (Python `gaierror`; `git ls-remote` exit 128).
- No browser binary is installed; no browser profile directory exists; no `~/.ssh`, no known_hosts, no Docker daemon, no mounts, no egress proxy found.
- Env contains only HOME/LANG/PATH/PWD; no auth/cookie/token/variable of any kind.
- Installed relevant packages: `requests`, `httpx2` only (no openai/playwright/selenium).
- Repo branch/base: `research/utb-m0-chat-history-capture` @ `516b3f8`, clean at start.

**INFERENCE**
- The workspace is an offline repository-execution sandbox, not the VPS runtime assumed by contract §4 (no profile, no network route to the provider).
- Because the contract’s stop condition mandates stopping on an environment blocker, live tests were halted rather than faked; this is the conservative interpretation of “stop that path”.

**HYPOTHESIS (testable later, not measured in M0 — carried over from DECISIONS.md H-001…H-006, unmodified)**
- H-001…H-006 remain open; no M0-derived data supports or refutes any of them.

**Deliberately NOT claimed**
- no PASS/PARTIAL/FAIL for any provider check; no auth-lifetime value; no endpoint/schema shapes; no rate-limit numbers; no MCP correlation.

---

## 6. Limitations and gaps

1. **Primary blocker:** no network egress and no VPS Chromium profile in the execution workspace. All provider-facing tests are unavailable here.
2. **Reuse-first inspection blocked:** upstream repos could not be cloned/ls-remote’d (`github.com` DNS failure). The reuse inventory (`UTB-M0-REUSE-INVENTORY.md`) is therefore **prior-knowledge only and explicitly unverified** — it must be re-verified on a networked runtime before M1 uses any code path.
3. **Owner-dependent steps not performed:** Test B requires the user to create an Android-only update in a disposable chat without opening it on Web; this was not possible from an offline sandbox and remains an owner-dependent gap for the coordinator to run on the real device/VPS.
4. **No measured RAM/auth/rate data:** browser RAM, auth lifetime, and 429 behavior columns remain empty by design; no values were invented.
5. **Re-run requirement:** to unblock, the M0 contract must be executed in the actual VPS runtime (network egress + existing authenticated Chromium profile), or the profile plus a browser must be provisioned into a networked executor. If that is impossible, M0 must be explicitly re-scoped/blocked by the Canonical Architect.

---

## 7. Deliverables and commit

- This report: `docs/research/UTB-M0-EVIDENCE.md`
- Reuse inventory: `docs/research/UTB-M0-REUSE-INVENTORY.md`
- Capture options: `docs/research/UTB-M0-CAPTURE-OPTIONS.md`
- Probe artifacts (secret-free): `experiments/m0/probe_env.py`, `experiments/m0/probe_env2.py`, `experiments/m0/probe_env3.py`, `experiments/m0/probe_env4.py`, `experiments/m0/README.md`
- Commit SHA: see git commit produced in this spike (reported in terminal handoff).

**Privacy/scope checks:** no credentials, cookies, tokens, `cf_clearance`, browser profiles, or raw private transcript content were collected, printed, or committed. Probe output contains environment presence/names only. No production collector, journal, database, memory integration, semantic state, continuity skills, Bridge/Codex integration, polling daemon, or M1 scaffolding was created. No write/generation endpoint was called (no network); no CAPTCHA/rate-limit bypass attempted.