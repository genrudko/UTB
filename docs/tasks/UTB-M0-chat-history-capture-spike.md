# UTB-M0 — ChatGPT History Capture Feasibility Spike

**Project:** Under the Bridge 🌉  
**Type:** bounded research spike  
**Owner:** Canonical Architect  
**Status:** READY  
**Date:** 2026-09-08  

## 1. Goal

Determine whether ChatGPT conversation history can be collected autonomously from the VPS for this real Plus account, including Android-only activity and multiple concurrently active conversations, **without depending on the home PC and without requiring a permanently running Chromium process**.

M0 produces evidence and a capture recommendation. It does **not** build production continuity or memory infrastructure.

## 2. Primary architectural questions

M0 must answer with measured evidence:

1. Can the VPS obtain the account's recent ChatGPT conversation list using existing authenticated state?
2. Does a conversation updated only from Android become visible to the same account-wide history path without opening that chat on Web?
3. Can one account-wide discovery mechanism distinguish 4–5 conversations updated in parallel?
4. How are normal chats, branches/versions, Project chats, and long conversations represented by the current provider responses?
5. Can the existing VPS Chromium profile bootstrap/refresh authentication and then terminate while a lightweight HTTP client continues history reads?
6. How long does usable HTTP authentication actually survive after Chromium exits?
7. Which auth component fails first in practice: access token, session cookie, Cloudflare/browser state, provider endpoint/schema, or something else?
8. What rate-limit behaviour appears under **conservative incremental read-only workload**, not bulk export?
9. Can changed conversations be discovered without repeatedly refetching the full account history?
10. Is there any observable timing correlation between ephemeral VPS browser/wake activity and the existing ChatGPT MCP tool-exposure/disappearance problem?

Question 10 is observational only. M0 must not turn into an MCP repair task.

## 3. Reuse-first mandate

Do not begin by implementing a ChatGPT client.

Evaluate existing open-source implementations first, especially code covering:

- ChatGPT session/auth acquisition;
- conversation listing;
- conversation detail/history fetch;
- incremental/resumable export;
- retry/backoff;
- branch/tree or current-path extraction;
- Project conversation discovery;
- raw JSON preservation.

Known candidates from preliminary research include projects such as:

- `FrankCJones/chatgpt-export`;
- `joningi/chatgpt-export`;
- `nborwankar/aishell`;
- other current ChatGPT exporters discovered during the spike.

The executor must record for every useful upstream component:

```text
AS-IS usable
ADAPTER needed
EXTRACT useful module
FORK candidate
NOT useful
```

Writing new provider-access code is allowed only if no reusable implementation can answer the required probe.

## 4. Environment assumptions

Known starting conditions:

- repository: `genrudko/UTB`;
- target runtime: existing VPS;
- an authenticated ChatGPT browser profile already exists on the VPS for the wake/bind mechanism;
- that browser is normally launched ephemerally and closed after wake/bind work;
- user may run multiple ChatGPT chats in parallel;
- Android usage is a first-class acceptance surface;
- home PC must not be required.

Do not assume a permanently running browser is acceptable merely because one already exists for ephemeral wake work.

## 5. Allowed scope

M0 may:

- clone/run/read existing open-source exporters and clients;
- use throwaway experiment code;
- inspect current ChatGPT history responses for this account;
- use the existing VPS ChatGPT browser profile for auth/bootstrap/refresh experiments;
- make conservative **read-only** history requests;
- save sanitized/raw experimental JSON outside Git or in explicitly ignored local experiment storage;
- measure process RAM, request cadence, HTTP statuses, auth lifetime, provider response shape, message IDs, and timestamps;
- add small reusable probe code under an experiment-only path if useful to reproduce evidence;
- document upstream code locations that can later be reused.

## 6. Forbidden scope

M0 must **not**:

- integrate Remnic or another production memory backend;
- implement a production raw journal/database;
- build semantic summaries or rolling state;
- invoke Antigravity/LLM workers for memory extraction;
- implement `continuity_resume`;
- implement continuity skills;
- integrate Bridge/Codex as continuity sources;
- build a permanent polling daemon/service;
- create Full-Pack architecture or production scaffolding;
- automate CAPTCHA/challenge bypass;
- ignore provider `Retry-After` or deliberately defeat rate limits;
- use write/generation endpoints through a private ChatGPT API;
- commit credentials, cookies, access tokens, `cf_clearance`, browser profiles, or raw private chat content;
- repair unrelated MCP/wake bugs;
- begin M1 automatically.

If a probe encounters a provider protection/challenge that cannot be handled by normal authenticated browser refresh and conservative retry/backoff, record it as evidence and stop that path rather than escalating into bypass work.

## 7. Required test sequence

### Test A — Baseline account-wide listing

- Obtain the current recent conversation list from VPS-side authenticated context using the least invasive reusable method found.
- Record endpoint/transport class, response shape, relevant IDs/timestamps, request count, status codes, and whether Chromium was required during the request.
- Sanitize evidence before committing documentation.

**Pass:** recent conversations can be enumerated reliably enough to identify individual conversations and their update ordering.

### Test B — Android-only update

1. Choose/create a disposable conversation.
2. Ensure the target test change occurs **only in Android**.
3. Do not open that conversation in ChatGPT Web before the VPS probe.
4. Poll/discover using the tested account-wide mechanism.
5. Fetch enough history to prove the Android-created turn is present.

**Pass:** the VPS sees the Android-only update with stable provider identity/order.

### Test C — Parallel conversations

Use 4–5 disposable/low-risk conversations updated close together from available ChatGPT surfaces.

**Pass:** the collector path identifies each changed conversation independently without one browser/tab per chat and without mixing turns.

### Test D — Branch/version representation

Use a disposable conversation with an explicit branch/edit/version where possible.

Record:

- conversation ID behaviour;
- message IDs;
- parent/child/version fields if present;
- active/current branch representation;
- whether old branches remain retrievable.

**Result:** PASS/PARTIAL/FAIL with exact observed provider semantics. No assumptions from old API documentation.

### Test E — Project conversation representation

Use a disposable conversation inside a ChatGPT Project.

Record how Project membership and conversation discovery are represented by current responses.

**Result:** PASS/PARTIAL/FAIL.

### Test F — Long conversation behaviour

Inspect at least one sufficiently long disposable or safe existing conversation to determine whether current provider responses use:

- full message tree;
- limited recent turns;
- pagination;
- current-path-only delivery;
- another shape.

Do not bulk-download sensitive history merely to satisfy this test.

### Test G — Browser-close / HTTP-lifetime measurement

1. Refresh/bootstrap auth using the existing VPS Chromium profile if required.
2. Close Chromium fully.
3. Continue conservative read-only HTTP probes.
4. Record successful duration and exact failure mode when/if it expires.

Take observations over the practical duration available to the executor. If full credential lifetime exceeds the bounded spike window, report a lower bound rather than waiting indefinitely.

Example:

```text
HTTP usable after Chromium exit: >= 6h observed
ultimate expiry: not observed during spike
```

Do not invent an expiry value.

### Test H — Ephemeral auth refresh

If HTTP auth becomes unusable during the spike:

1. launch existing Chromium profile;
2. establish normal authenticated ChatGPT state;
3. refresh/re-extract only what the reusable client legitimately requires;
4. close Chromium;
5. retry the same HTTP read.

**Pass:** a bounded browser launch restores the lightweight read path without a permanently running browser.

If expiry is not observed, report this test as NOT TRIGGERED rather than forcing failure.

### Test I — Incremental/rate behaviour

Run a conservative changed-conversation discovery pattern representative of UTB, not a bulk export benchmark.

Record:

- polling interval;
- request count;
- concurrency;
- statuses;
- `Retry-After`/429 if any;
- whether unchanged conversations can be skipped;
- whether full conversation bodies must be re-fetched after every update.

No stress testing is required.

### Test J — MCP correlation observation

During normal M0 work only, timestamp:

- VPS Chromium launches/closes;
- wake/bind browser activity if it naturally occurs;
- observed ChatGPT MCP tool-exposure disappearance/recovery if it naturally occurs.

Do not manufacture extensive MCP failure testing unless it is nearly free and non-disruptive.

**Deliverable:** `correlation observed`, `no correlation observed`, or `insufficient evidence` — never a causal claim without evidence.

## 8. Acceptance matrix

The final evidence report must contain this table with measured values:

| Check | Result | Evidence |
|---|---|---|
| VPS conversation list | PASS/FAIL | transport/endpoint class + sanitized sample |
| Android-only update visible | PASS/FAIL | timestamps/provider IDs |
| 4–5 parallel chats | PASS/FAIL | distinct conversation IDs/update ordering |
| Branch/version semantics | PASS/PARTIAL/FAIL | observed response fields |
| Project chat semantics | PASS/PARTIAL/FAIL | observed response fields |
| Long-chat retrieval semantics | PASS/PARTIAL/FAIL | pagination/turn behaviour |
| Chromium closed → HTTP works | PASS/FAIL | observed duration |
| Auth lifetime | value/lower bound/unknown | observations only |
| Ephemeral refresh | PASS/FAIL/NOT TRIGGERED | exact procedure/result |
| Incremental discovery | PASS/PARTIAL/FAIL | request pattern |
| 429/rate behaviour | observed/not observed | cadence/statuses |
| Browser RAM peak | measured | RSS/available-memory snapshot |
| Steady-state browser RAM | measured | target: browser terminated |
| MCP correlation | observed/none/insufficient | timestamps only |

## 9. Required deliverables

### A. `docs/research/UTB-M0-EVIDENCE.md`

Must contain:

- test environment;
- exact test sequence actually performed;
- sanitized evidence;
- acceptance matrix;
- limitations/gaps;
- FACT vs INFERENCE separation.

### B. `docs/research/UTB-M0-REUSE-INVENTORY.md`

For each upstream examined:

- repository/version/commit if practical;
- which components are useful;
- reuse classification (`AS-IS`, `ADAPTER`, `EXTRACT`, `FORK`, `NOT USEFUL`);
- maintenance/stability observations;
- code paths/functions worth reusing.

### C. `docs/research/UTB-M0-CAPTURE-OPTIONS.md`

Compare at minimum:

- HTTP-only;
- HTTP + ephemeral Chromium auth refresh;
- ephemeral Chromium fetch;
- MCP-only realtime capture;
- hybrid realtime + reconciliation.

Evaluate:

- Android coverage;
- autonomy;
- steady-state RAM;
- auth complexity;
- reliability;
- maintenance burden;
- account/provider risk signals observed during M0;
- amount of own code required.

This document recommends; it does not silently create a canonical decision.

### D. Optional throwaway/reusable probe artifacts

If code is required to reproduce evidence, keep it clearly experiment-scoped, small, documented, and free of secrets/private transcript content.

## 10. Stop condition

When A–C are complete and the acceptance matrix is filled, **STOP**.

Do not:

- choose M1 implementation unilaterally;
- productionize a collector;
- deploy a permanent service;
- integrate memory;
- continue into skills/Bridge/Codex work.

Return the evidence to the Canonical Architect for adjudication. The Canonical Architect will record any resulting architecture decision and issue the bounded M1 contract.

## 11. Success criterion for M0

M0 succeeds as a research stage if it reduces the capture architecture uncertainty with trustworthy evidence — even if the result disproves the currently attractive HTTP/ephemeral-browser hypotheses.

The spike is **not** required to prove that the preferred architecture works. It is required to tell the truth about what works.
