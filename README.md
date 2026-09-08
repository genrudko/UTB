# Under the Bridge 🌉

**Under the Bridge (UTB)** is a personal AI continuity infrastructure project. Its first job is simple: make it possible to abandon a degraded, full, or broken ChatGPT conversation and continue in a new one without manually re-explaining the work.

UTB is not intended to become a general-purpose enterprise memory platform. The project optimizes for practical continuity, reliability, stability, low operational cost, and aggressive reuse of existing open-source components.

## Product direction

UTB is built in two levels:

1. **Minimal Seamless Continuity** — autonomously capture conversation history, maintain a compact working state, and resume in a new chat.
2. **Full Pack** — add durable cross-conversation memory, workflow skills, Codex/Bridge integration, reconciliation, and optional coordinator surfaces such as GPTs/Projects.

The Minimal layer must become useful early and then dogfood itself during development of the Full Pack.

## Canonical principles

- **Reuse first.** Prefer upstream as-is → adapter → extracted module → fork → own implementation.
- **Raw evidence first.** Raw conversation history and structured runtime events must remain recoverable independently of semantic summaries.
- **Semantic state is derived.** Rolling continuity state and long-term memory may be rebuilt from evidence.
- **No home-PC dependency.** The required runtime must remain available when the user's home computer is off.
- **Minimal before Full Pack.** Do not start a broad memory platform before seamless handoff works.
- **No enterprise theatre.** Personal-use baseline security is limited to practical hygiene such as protecting credentials, authenticated access, backups, idempotency, and recovery.
- **Evidence before architecture changes.** New findings are facts or hypotheses until explicitly promoted to a decision.

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Canonical decisions

See [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Current stage

**UTB-M0 — ChatGPT History Capture Feasibility**

The first research gate tests whether ChatGPT conversation history can be collected autonomously from the VPS, including Android-only activity and parallel conversations, without depending on the home PC or a permanently running Chromium process.

Task contract: [`docs/tasks/UTB-M0-chat-history-capture-spike.md`](docs/tasks/UTB-M0-chat-history-capture-spike.md).
