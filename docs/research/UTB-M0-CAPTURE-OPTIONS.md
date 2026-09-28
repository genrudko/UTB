# UTB-M0 — Capture Options Comparison

**Stage:** UTB-M0
**Status:** ⚠️ **No measured data — live tests A–J were BLOCKED in the provided execution sandbox** (no network egress, no browser, no authenticated ChatGPT profile). See `UTB-M0-EVIDENCE.md` §1/§4.
**Scope guard:** this document compares and, where possible, provisionally ranks options. It **does not create a canonical architecture decision** (DECISIONS.md D-009 remains authoritative: capture transport is unresolved until M0 evidence exists).

---

## 0. How to read this document

- Every cell that depends on live provider observation is marked **NO DATA (M0 blocked)**.
- Qualitative reasoning that does not depend on the live account is labeled **[H] hypothesis-level desktop reasoning** — informed by general knowledge of the ChatGPT web backend and the ecosystem notes in `UTB-M0-REUSE-INVENTORY.md`, **not** by measurements on this account.
- **There is therefore no evidence-based recommendation.** The correct M0 outcome in this workspace is a blocker report, not a transport choice.

---

## 1. Options compared

| Option | Definition (per ARCHITECTURE.md §6 / contract) |
|---|---|
| O1 HTTP-only | Lightweight HTTP client reads account history using an existing authenticated session (token/cookies); no browser at runtime. |
| O2 HTTP + ephemeral Chromium auth refresh | HTTP-only steady state; launch existing VPS Chromium profile only to refresh/re-extract auth when HTTP auth fails; close it after. |
| O3 Ephemeral Chromium fetch | Each capture cycle launches Chromium with the VPS profile, does the fetch in-browser, then closes Chromium. |
| O4 MCP-only realtime capture | Capture primarily from ChatGPT MCP tool events as they happen (realtime fast path), no history reconciliation implied. |
| O5 Hybrid realtime + reconciliation | MCP realtime events as fast path **plus** periodic HTTP history reconciliation for gaps/rows (matches F5 trajectory). |

---

## 2. Comparison table

Legend: `NO DATA` = not measured in M0 (blocked). `[H]` = hypothesis-level reasoning, not evidence. Ratings are 0–3 scale for direction only.

| Dimension | O1 HTTP-only | O2 HTTP + ephemeral refresh | O3 ephemeral fetch | O4 MCP-only | O5 hybrid |
|---|---|---|---|---|---|
| Android coverage | NO DATA; [H] account-wide history should include Android-originated turns if same account/server-side store — **must be proven by Test B on VPS** | same as O1 (both depend on account-wide history incl. Android) | [H] same store, but browser-fetch adds UI-context dependency; still needs Test B | [H] Android activity produces no MCP events from web-side tooling → **likely blind on Android-only updates** unless app-side events exist (none seen) | [H] O4 blind spot on Android closed by O1/O2 reconciliation; still needs Test B |
| Autonomy (no home PC / permanent browser) | [H] fully headless, no browser runtime — highest autonomy; requires session lifetime to hold (Test G) | [H] headless steady state; needs periodic bounded browser wakes (Test H) — still fully VPS-autonomous | [H] requires Chromium runtime per cycle; heavier but still VPS-only | [H] requires a live MCP-capable ChatGPT session/client; depends on external tool stability (H-006) | [H] server-driven; autonomy high if O1/O2 limb works |
| Steady-state RAM | [H] lowest (HTTP client RSS) — **NO DATA: browser RAM unmeasured (no browser in sandbox)** | [H] low (HTTP) + browser only during refresh windows | [H] high per cycle (browser RSS while cycling) — unmeasured | [H] depends on MCP client runtime (could be high if browser-mediated) | [H] low base + event listener; worst-case = O2 cycle |
| Auth complexity | [H] highest risk: tokens/cookies/cf state expiry; Cloudflare challenges unhandleable without browser (H-001/H-005; ecosystem history in reuse inventory) | [H] medium: reuse existing profile; refresh only on failure; must not fight challenges beyond normal refresh (contract rule) | [H] medium-low (browser handles auth) but repeats challenge overhead each cycle | [H] delegated to MCP client/login; but external lifecycle bugs (H-006) create hidden coupling | [H] inherits O2 complexity + event listener bookkeeping |
| Reliability | NO DATA (Test G/I); [H] session lifetime is the single point of failure | NO DATA; [H] refresh adds a recovery path → better reliability than O1 if refresh works (Test H) | [H] reliable auth-wise but more moving parts/RAM; risk of profile lock/contention | [H] lowest standalone reliability: missing events are silently lost without reconciliation | [H] best worst-case: reconciliation repairs realtime gaps (TRACK F5) |
| Maintenance burden | [H] low surface, but high exposure to endpoint shape changes (versioned adapters) | [H] moderate: HTTP adapter + bounded browser-launch automation | [H] high: browser automation upkeep (selectors/cf changes) | [H] high external coupling; depends on ChatGPT MCP lifecycle that is already unstable (H-006) | [H] highest upfront (two paths), but each path is simpler and failure-isolable |
| Observed provider/account risk signals during M0 | **none observed — M0 blocked; no requests made** (no 429/Retry-After evidence, no challenge evidence) | same | same | same | same |
| Own-code burden (reuse-first) | [H] low-medium: reuse upstream list/detail/branch fetch (inventory items 1–2) behind adapter | [H] medium: adapter + small launch/refresh glue (profile exists on VPS) | [H] medium-high: browser automation glue or upstream userscript reuse (inventory item 6) | [H] protocol glue to MCP (depends on provider MCP surface; forbidden to repair in M0) | [H] highest own code (two limbs + watermark/reconciliation) |
| Aligns with forbidden scope | ✅ no write endpoints; must respect Retry-After | ✅ same + bounded refresh only | ✅ same | ⚠️ must be read-only/capture-only; careful not to turn MCP into production daemon in M0 | ✅ if built read-only; reconciliation is F5 territory (later) |

---

## 3. Risk signals recorded during M0 (all = none observed, truthfully)

| Signal | Observation |
|---|---|
| 429 / Retry-After | **not observed — zero requests possible (blocked)** |
| Cloudflare challenge on HTTP | **not observed — blocked before any request** |
| Session/token expiry (Test G) | **not observed — no auth existed in sandbox** |
| MCP instability correlation (Test J) | **insufficient evidence** (no browser/wake activity in sandbox) |

No provider or account risk signal can be claimed from this spike. The coordinator must not treat any option as validated.

---

## 4. Recommendation

**No evidence-based recommendation is possible from this workspace.** All live measurements (A–J) are BLOCKED; D-009 remains in force.

Provisional working hypotheses for the coordinator to test on the real VPS (clearly **not** decisions):

1. Start M0 re-run with **O2 (HTTP + ephemeral Chromium refresh)** as the primary hypothesis to falsify, because it bounds steady-state RAM (target: browser terminated — matches contract Test G/H and D-004), preserves a normal-browser recovery path for Cloudflare/auth changes, and matches the existing VPS profile setup. This is a hypothesis, not a choice.
2. Require Tests B and C **before** any architecture lean: Android visibility and parallel-chat discrimination are the two acceptance-critical unknowns.
3. Treat O4 (MCP-only) as a complement, not a sole path, pending Test J evidence; reconciliation (O5) is F5 trajectory and must not be built in M0/M1.
4. Re-verify the reuse inventory on a networked runtime before writing any provider-access code (M1 gate per task contract §3).

If the VPS runtime cannot be provided for a re-run, M0 must be explicitly closed as BLOCKED by the Canonical Architect; the acceptance matrix in `UTB-M0-EVIDENCE.md` already records the blocking environment facts so the re-run is reproducible.

---

## 5. What must be measured to unblock a recommendation

- Test A: endpoint class + response shape + whether Chromium is needed per request.
- Test B: Android-only update visibility with true provenance (never opened on Web first).
- Test C: 4–5 parallel chats distinguishable in one discovery pass.
- Test D/E/F: branch/version, Project, and long-chat semantics in today’s responses.
- Test G/H: Chromium-close → HTTP lifetime (lower bound) and refresh restore.
- Test I: conservative incremental cadence, 429/Retry-After, unchanged-skip, full-body-refetch need.
- Test J: MCP correlation timestamps only.

Until then, **no row in the acceptance matrix may be treated as valid evidence**, and no option is recommended.