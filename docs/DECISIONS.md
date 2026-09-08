# Under the Bridge — Decision Log

**Status:** Canonical decision log v0.1  
**Date:** 2026-09-08  

UTB distinguishes observations from commitments. Use these labels consistently:

- **FACT** — directly observed or verified;
- **EVIDENCE** — practical data supporting a claim;
- **INFERENCE** — a reasoned conclusion not directly verified;
- **HYPOTHESIS** — a testable possibility;
- **DECISION** — an explicitly accepted architectural commitment.

A new fact, source, bug report, or hypothesis does not automatically reverse a decision. Architecture changes require an explicit new decision that explains why the previous one is superseded.

---

## Accepted decisions

### D-001 — UTB is a standalone project

**Status:** DECISION  
**Date:** 2026-09-08

Under the Bridge is maintained independently of Development Bridge, Fusion, EOD, or any single application repository.

**Reason:** continuity/memory/workflow infrastructure is cross-project and must remain independently replaceable and testable.

---

### D-002 — Reuse first

**Status:** DECISION  
**Date:** 2026-09-08

For every subsystem, prefer:

```text
upstream as-is
→ thin adapter
→ extracted upstream module
→ fork
→ own implementation
```

Own implementation is the last option, not the default.

**Reason:** maximize useful output while minimizing development and maintenance cost.

---

### D-003 — Raw evidence is not replaced by semantic summaries

**Status:** DECISION  
**Date:** 2026-09-08

Conversation summaries, rolling state, and long-term memory are derived artifacts. Raw conversation/provider evidence and structured authoritative events must remain recoverable independently.

**Reason:** semantic processing can be wrong, stale, unavailable, or changed later; evidence must allow reconstruction.

---

### D-004 — The home PC is not a required runtime component

**Status:** DECISION  
**Date:** 2026-09-08

UTB's required runtime must continue operating while the user's home computer is off or unreachable.

A home-browser extension may exist as an optional accelerator or diagnostic aid but cannot be required for continuity.

---

### D-005 — Minimal Seamless Continuity precedes Full Pack

**Status:** DECISION  
**Date:** 2026-09-08

UTB first solves chat-to-chat continuity. Durable cross-conversation memory, deep Bridge/Codex integration, broad skills packaging, and historical import must not become prerequisites for Minimal.

**Reason:** early utility and dogfooding reduce continuity risk during development of the larger system.

---

### D-006 — Semantic state may lag raw history, but freshness must be explicit

**Status:** DECISION  
**Date:** 2026-09-08

Continuity state is allowed to be asynchronous. It must expose enough information to determine which raw messages/turns it covers, such as `raw_through` and `state_through` markers.

If semantic processing is behind, resume must consume the uncovered raw tail rather than silently presenting stale state as current.

---

### D-007 — Procedure, capability, memory, and truth are separate concerns

**Status:** DECISION  
**Date:** 2026-09-08

Use the following conceptual ownership:

| Concern | Canonical location |
|---|---|
| role / entry surface | ChatGPT Project / GPT / client configuration |
| stable workflow procedure | Skills |
| actions/capabilities | Plugins / Apps / MCP |
| conversation working state | Continuity |
| durable cross-conversation knowledge | Long-term Memory |
| technical evidence/current truth | raw provider data / Git / Bridge / runtime |

Do not store volatile operational state in Skills or GPT instructions.

---

### D-008 — Personal-use security posture

**Status:** DECISION  
**Date:** 2026-09-08

UTB intentionally avoids enterprise-security scope unless a concrete later requirement appears.

Baseline hygiene remains mandatory:

- no credentials/session secrets committed to Git;
- authenticated remote surfaces;
- practical credential protection;
- backup/recovery;
- bounded/idempotent operations where relevant.

Explicitly not baseline requirements: RBAC, multi-tenancy, governance/compliance frameworks, enterprise audit design.

---

### D-009 — Capture transport remains unresolved until M0 evidence

**Status:** DECISION  
**Date:** 2026-09-08

UTB does not yet commit to HTTP-only history sync, ephemeral Chromium-assisted auth, browser-based fetch, MCP turn capture, or a hybrid.

**Reason:** capture behaviour must be measured on the real Plus/VPS/Android environment before selecting the production design.

---

### D-010 — GPT/Project coordinator surfaces are optional and non-canonical

**Status:** DECISION  
**Date:** 2026-09-08

GPTs/Projects may provide a stable role/entry point and package skills/tools, but UTB state and evidence must survive their removal or recreation.

---

### D-011 — Architecture does not pivot on a single new signal

**Status:** DECISION  
**Date:** 2026-09-08

During research, new observations are recorded as FACT/EVIDENCE/INFERENCE/HYPOTHESIS. They become architecture only through an explicit DECISION after considering competing evidence, implementation cost, reliability, and reversibility.

**Reason:** prevent impulsive architecture churn during exploratory work.

---

## Open hypotheses for UTB-M0

These are **not decisions**.

### H-001 — VPS HTTP sync can read conversation history after browser authentication

A lightweight HTTP client may be able to continue reading account history after the VPS Chromium process is terminated.

**Need:** measure auth/session lifetime and failure mode.

### H-002 — Android-only activity is visible through account-wide server history

A conversation updated only in the Android app may appear in the same server-side history that Web clients use.

**Need:** controlled Android-only test without opening the conversation on Web.

### H-003 — One account-wide sync can cover multiple parallel chats

A single recent-conversations discovery pass may identify all currently changed conversations without one browser/tab per chat.

**Need:** 4–5 parallel conversation test.

### H-004 — Chromium can be an ephemeral auth-refresh mechanism

The existing VPS browser profile may be usable only when auth refresh is required, allowing Chromium to exit during steady-state sync.

**Need:** repeated browser-close / HTTP-sync / refresh cycles.

### H-005 — Conservative read-only incremental sync is operationally sustainable

Low-concurrency, change-only reads with normal backoff may avoid problematic rate-limit behaviour seen by bulk exporters.

**Need:** measure actual request cadence and 429/403/auth behaviour; do not infer from bulk-export workloads.

### H-006 — VPS ChatGPT browser launches may correlate with MCP tool-exposure instability

Different concurrent account/network sessions could be a contributor to current MCP disappearance behaviour, but existing evidence also supports an independent ChatGPT MCP lifecycle bug.

**Need:** observation/correlation only during M0. M0 does not repair MCP.

---

## Supersession policy

When a decision changes, do not silently edit the old rationale away. Add a new decision entry that explicitly states:

- which decision it supersedes;
- what new evidence changed the balance;
- migration/compatibility impact;
- whether the old path remains as fallback.
