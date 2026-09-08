# Under the Bridge — Roadmap

**Status:** Canonical roadmap v0.1  
**Date:** 2026-09-08  

UTB develops in two layers. **Minimal Seamless Continuity is mandatory first. Full Pack may only build on a working Minimal.**

---

# Track A — Minimal Seamless Continuity

## M0 — ChatGPT History Capture Feasibility

**Goal:** determine whether ChatGPT conversation history can be collected autonomously from the VPS, including Android-only activity and parallel chats, without depending on the home PC or a permanently running Chromium process.

**Nature:** research spike; evidence only.

**Reuse target:** existing ChatGPT exporters/clients/auth code before custom implementation.

**Gate:** a measured capture strategy recommendation based on the real Plus/VPS/Android environment.

Task contract: [`tasks/UTB-M0-chat-history-capture-spike.md`](tasks/UTB-M0-chat-history-capture-spike.md).

---

## M1 — Raw Conversation Collector

**Goal:** create a resumable, idempotent collector that stores raw conversation evidence and provider metadata for changed chats.

Expected scope:

- account-wide changed-conversation discovery;
- provider message/turn identity;
- ordering and deduplication;
- branch/version metadata where available;
- Project chat identification where available;
- raw provider payload preservation;
- sync watermarks;
- retry/backoff based on M0 evidence.

**Reuse target:** adapt upstream exporter code instead of writing provider access from scratch.

**Gate:** repeated sync and restart do not lose, reorder, or duplicate canonical conversation data across multiple active chats.

---

## M2 — Rolling Continuity State

**Goal:** derive compact structured state from raw conversation deltas without making semantic state the source of truth.

Expected state:

- current focus;
- relevant facts;
- decisions;
- corrections;
- rejected/failed approaches;
- unresolved questions;
- next likely step;
- `raw_through` and `state_through` freshness markers.

**Runtime inference target:** low-cost/minimal-effort model such as Antigravity-class processing; model choice remains configurable.

**Gate:** the state remains practically accurate across representative technical and non-technical conversations and can be rebuilt from raw evidence.

---

## M3 — Seamless Resume

**Goal:** expose one simple resume operation that produces a bounded handoff packet for a new chat/session.

Resume input combines:

```text
latest structured state
+
unprocessed raw tail
+
small recent verbatim tail
```

A small `continuity-and-recovery` skill/procedure may be added so a new session uses the resume operation correctly rather than asking the user to reconstruct state manually.

**Gate:** abandon a live conversation without a handoff summary, open a new one, and continue with at least 95% of practically relevant context; omitted details remain retrievable from raw history.

---

## M4 — Dogfood and Minimal Stabilization

**Goal:** use UTB Minimal to continue development of UTB itself across chat boundaries.

Stabilization scope only:

- restart recovery;
- backlog/freshness visibility;
- basic backups;
- idempotency fixes;
- bounded auth refresh handling if required by the selected M0 architecture;
- acceptance on Web and Android-originated conversations.

**Gate / Minimal Definition of Done:** a chat can end unexpectedly during real UTB work and a new chat can resume without a manually prepared summary or replaying the whole transcript into context.

---

# Track B — Full Pack

Full Pack starts only after Minimal is accepted and already dogfooding UTB development.

## F0 — Minimal Accepted

Dependency gate, not an implementation milestone.

No Full-Pack subsystem may become a prerequisite for basic chat-to-chat continuity.

---

## F1 — Workflow Skills Foundation

**Goal:** separate stable procedures from tools and volatile project state.

Initial candidates:

- `continuity-and-recovery`;
- `bridge-task-orchestrator`;
- `review-adjudication`;
- `project-closeout`;
- `executor-selection`.

Domain skills may later include Fusion CAD and EOD engineering rules.

**Reuse target:** use existing Superpowers/OpenAI skill mechanisms where practical; write only UTB/project-specific procedure layers.

**Gate:** a fresh session not only knows current state but follows the accepted continuation/review/orchestration procedure without repeated manual instruction.

---

## F2 — Shared Memory Backend Evaluation and Integration

**Goal:** select and integrate a reusable cross-client memory backend rather than implement one from scratch.

Primary candidate: Remnic; alternatives remain open until measured.

Evaluate:

- shared HTTP/MCP runtime;
- transcript compatibility;
- search/retrieval;
- corrections/provenance;
- Codex integration;
- rebuild/recovery behaviour;
- operational footprint.

**Gate:** one backend can serve multiple clients without becoming a second conflicting source of truth.

---

## F3 — Durable Cross-Conversation Memory

**Goal:** promote selected conversation knowledge into durable reusable memory.

Candidate types:

- stable facts;
- preferences;
- environment/capability facts;
- decisions;
- constraints;
- failed approaches;
- user corrections;
- project-level state useful across conversations.

Durable memory remains derived and source-linked; raw evidence remains recoverable.

**Gate:** a genuinely new independent conversation retrieves relevant durable context without inheriting stale or superseded facts as current truth.

---

## F4 — Development Continuity: Codex / Bridge / Git

**Goal:** combine conversation-derived continuity with structured authoritative development events.

Expected integrations:

- Codex/session hooks where available;
- Bridge job lifecycle;
- commits/branches/tests/reviews;
- continuation/wake state;
- runtime verification.

**Gate:** a chat/session can disappear during a long development task and the next session reconstructs actual operational state without repeating completed work.

---

## F5 — Cross-Source Reconciliation

**Goal:** detect and repair gaps between realtime MCP events, provider conversation history, Bridge/Codex events, and semantic state.

Examples:

```text
state through turn 101
provider history through turn 104
→ backfill 102–104
```

or

```text
chat summary: job complete
Bridge live state: running
→ live structured state wins
```

**Gate:** deliberately missed realtime events are recoverable from authoritative sources and conflicts are visible rather than silently merged.

---

## F6 — Historical Bootstrap

**Goal:** import useful prior history only after the live system proves itself.

Start with high-value corpora/projects rather than the entire account.

**Reuse target:** existing ChatGPT import/export tooling and memory-backend importers.

**Gate:** imported material improves retrieval without polluting current state with stale decisions or duplicate facts.

---

## F7 — Coordinator Surface

**Goal:** provide an optional stable entry surface (for example a GPT/Project/plugin package) that combines role, skills, tools, continuity, and memory.

This surface is not canonical storage and must be replaceable without losing UTB state.

**Gate:** a coordinator surface can be removed/recreated while continuity and memory remain intact.

---

## F8 — Full-Pack Hardening

Only demonstrated operational needs belong here:

- backup/restore;
- integrity checks;
- auth refresh/recovery;
- health/backlog indicators;
- retry/idempotency;
- provider-adapter compatibility tests;
- bounded operational logging.

Explicitly excluded unless future evidence creates a concrete requirement:

- enterprise RBAC;
- multi-tenancy;
- compliance/governance frameworks;
- knowledge-graph platforms;
- vector databases/embeddings without proven retrieval need;
- custom mobile applications;
- replacement ChatGPT UI;
- decorative dashboards.

---

# Stage discipline

Every implementation stage must have:

1. a bounded goal;
2. explicit allowed and forbidden scope;
3. reuse inventory before own implementation;
4. measurable acceptance criteria;
5. evidence deliverables;
6. a stop condition that prevents automatically starting the next stage.

The Canonical Architect reviews stage evidence and issues the next task contract.
