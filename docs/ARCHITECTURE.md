# Under the Bridge — Canonical Architecture

**Status:** Canonical baseline v0.1  
**Date:** 2026-09-08  
**Authority:** Canonical Architect  

## 1. Problem statement

Long-running AI work is currently coupled too tightly to individual chat sessions. Chats can hit practical context limits, degrade in UI behaviour, lose connector exposure, fail to load cleanly, or simply become inconvenient to continue. Reconstructing the state manually in a new conversation is slow, error-prone, and repeatedly destroys continuity.

UTB exists to separate **work continuity** from the lifetime of any single chat session.

## 2. Product goals

### Minimal goal

A new conversation can continue a previous conversation with little or no manual handoff. The system must recover the practically relevant working state and retain access to exact source history for anything the compact state omitted.

### Full-Pack goal

Build on Minimal to provide:

- durable cross-conversation personal/project memory;
- reusable workflow skills;
- shared context across ChatGPT, Codex, Bridge, and future compatible clients;
- structured reconciliation against authoritative runtime sources;
- optional coordinator surfaces such as GPTs/Projects without making them canonical stores.

## 3. Canonical layers

```text
┌──────────────────────────────────────────┐
│ ChatGPT / Project / Codex / GPT(optional)│  role / surface
├──────────────────────────────────────────┤
│ Skills                                   │  HOW to work
├──────────────────────────────────────────┤
│ Plugins / Apps / MCP                     │  WHAT tools can do
├──────────────────────────────────────────┤
│ Continuity + Long-term Memory            │  WHAT to remember
├──────────────────────────────────────────┤
│ Evidence / Canonical truth               │
│ raw chat / Git / Bridge / runtime        │  WHAT happened / is true
└──────────────────────────────────────────┘
```

These layers must remain separable. UTB must not turn Bridge, a GPT, or a memory backend into a monolith that simultaneously acts as tool gateway, policy engine, memory, workflow prompt, and source of truth.

## 4. Data semantics

### 4.1 Raw evidence

Raw provider conversation data and structured external events are the recoverable evidence layer.

Examples:

- ChatGPT conversation messages and provider metadata;
- branch/version relationships where exposed;
- Bridge durable job events;
- Git commit/branch state;
- Codex session/tool events;
- runtime verification results.

Raw evidence is preserved independently of semantic interpretation.

### 4.2 Continuity state

Continuity state is a compact, derived description of the current conversation/work state. Typical fields include:

- current topic/focus;
- important facts;
- decisions;
- corrections;
- rejected/failed approaches;
- unresolved questions;
- next likely action;
- recent verbatim tail;
- source pointers;
- freshness markers.

Continuity state is allowed to lag raw evidence. It must therefore expose at least:

```text
raw_through = <provider message/turn marker>
state_through = <provider message/turn marker>
```

If `raw_through > state_through`, resume must include or process the uncovered raw tail rather than pretending that the semantic state is current.

### 4.3 Long-term memory

Long-term memory is cross-conversation durable knowledge such as stable preferences, environment facts, corrections, project decisions, constraints, and repeatedly useful findings.

It is not the same thing as conversation continuity and must not be required for Minimal Seamless Continuity.

### 4.4 Skills

Skills store stable procedures: how to recover context, how to orchestrate Bridge work, how to adjudicate review findings, how to close out work, and domain-specific engineering rules.

Skills must not store volatile state such as current job IDs, task numbers, branch heads, or current PR status.

### 4.5 Plugins / MCP / Apps

These expose capabilities: fetch state, run jobs, read repositories, resume continuity, query memory, or mutate supported systems.

They should not carry the full workflow methodology when that methodology belongs in a skill.

## 5. Resume model

The intended Minimal resume path is:

```text
latest structured state
        +
raw messages after state_through
        +
small recent verbatim tail
        ↓
bounded resume packet
        ↓
new chat/session
```

A resume packet is a working map, not an immutable truth source. If a technical project has live structured state (Git/Bridge/runtime), that live state may supersede stale conversational interpretation.

## 6. Capture architecture — intentionally unresolved

UTB does **not** yet commit to one ChatGPT capture transport. UTB-M0 exists to measure the options on the real Plus/VPS/Android environment.

Current candidates:

1. **HTTP-only history sync** using an authenticated ChatGPT session state.
2. **HTTP + ephemeral Chromium refresh** where Chromium is launched only when auth must be refreshed and then terminated.
3. **Ephemeral browser fetch** using the existing VPS browser profile for short capture cycles.
4. **MCP turn protocol** as a realtime fast path, with later history reconciliation.
5. **Hybrid** combinations of the above.

The user's home PC is not an acceptable required runtime component.

## 7. Capture and interpretation are separate

```text
provider/raw sources
        ↓
mechanical collector
        ↓
raw journal
        ↓
semantic worker
        ↓
continuity state / memory candidates
```

The collector must not decide what is important. It is responsible for identity, ordering, deduplication, retry/reconciliation, raw preservation, and watermarks.

The semantic worker is allowed to be probabilistic because the evidence layer remains intact and rebuildable.

## 8. Source authority

For technical state, prefer direct evidence over derived summaries. A baseline ordering is:

```text
live verified state
    > structured system/tool event
    > explicit user statement
    > trusted external source
    > model-derived interpretation
```

This ordering is a default reasoning rule, not a replacement for conflict handling. Context-specific exceptions may exist and must be explicit.

## 9. Reuse-first integration policy

For every subsystem, use this order:

1. upstream project as-is;
2. thin adapter around upstream;
3. extract/reuse an upstream module;
4. fork only when upstream architecture blocks the requirement;
5. write new implementation only when the previous options fail.

Current upstream/reference candidates include Remnic, context-mode, ChatGPT exporters, and other mature session/memory tooling. No upstream is canonical until evaluated against UTB requirements.

## 10. Runtime model

Required runtime components should live on always-available infrastructure (currently the VPS), not on the home PC.

A heavyweight browser may be used ephemerally if needed, but a permanently running Chromium process is not assumed by the architecture.

## 11. Failure model

The system must degrade visibly and recoverably:

- raw capture can continue while semantic processing is down;
- semantic state can be rebuilt from raw history;
- duplicate provider fetches must be safe;
- interrupted sync must be resumable;
- stale semantic state must be detectable through freshness markers;
- unsupported/changed provider API shapes must fail as an adapter problem rather than corrupting canonical data.

## 12. Security posture

UTB is a personal-use system, not an enterprise product. Baseline security is intentionally limited to practical hygiene:

- do not commit credentials or session secrets;
- authenticate remote control/read surfaces;
- protect stored credentials from casual exposure;
- preserve backups/recovery paths;
- use idempotent and bounded operations where practical.

Enterprise features such as RBAC, multi-tenancy, governance workflows, compliance audit frameworks, or security architecture for its own sake are outside the baseline unless a concrete future requirement appears.

## 13. Non-goals for Minimal

Minimal does not include:

- vector databases or embeddings;
- knowledge graphs;
- global personal-memory extraction;
- historical import of the entire account;
- Bridge/Codex deep integration;
- dashboards;
- a custom mobile app;
- a replacement ChatGPT UI;
- multi-user support;
- enterprise governance/security layers.

## 14. Architecture change discipline

Every new observation is classified as one of:

- **FACT** — directly observed/verified;
- **EVIDENCE** — practical data supporting a claim;
- **INFERENCE** — a reasoned conclusion not directly verified;
- **HYPOTHESIS** — a testable possibility;
- **DECISION** — an explicitly accepted architectural commitment.

A new fact or hypothesis does not automatically reverse architecture. Decisions are updated only after weighing evidence and downstream cost.
