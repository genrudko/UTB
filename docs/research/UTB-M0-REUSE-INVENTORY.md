# UTB-M0 — Reuse Inventory: ChatGPT Exporters / Clients

**Stage:** UTB-M0
**Inspection status:** ⚠️ **BLOCKED at inspection time — no network in execution sandbox** (`github.com`/`raw.githubusercontent.com` DNS fail; `git ls-remote` exit 128; no pip index). Entries below are **prior-knowledge only and are NOT freshly verified in this spike.**
**Action required before reuse in M1:** re-verify each entry on a networked runtime (clone + read the exact commit) and update this inventory with real commit SHAs and verified code paths.

Classification legend (contract §3): `AS-IS` usable / `ADAPTER` needed / `EXTRACT` useful module / `FORK` candidate / `NOT USEFUL`.
Because inspection was blocked, every classification below is **TENTATIVE (prior knowledge)** and must be confirmed.

---

## 1. FrankCJones/chatgpt-export

- **Type:** Python CLI ChatGPT conversation exporter (pip-installable, e.g. `chatgpt_export` command).
- **Useful components (prior knowledge, approximate — verify paths):**
  - conversation **list** enumeration against the web backend history endpoint (`chatgpt.com`/`chat.openai.com` backend history API);
  - conversation **detail** fetch incl. message tree; JSON/Markdown/HTML output;
  - explicit **branch/version** handling (fetch branch (`tree`) + current node, export arbitrary branches);
  - **token/session** acquisition helpers incl. reading tokens from a local Chrome profile directory (`--chrome-data-dir`-style flag) — relevant to an ephemeral-browser refresh design;
  - incremental/selective export patterns (by conversation id, by project/folder where supported).
- **Tentative classification:** `ADAPTER` (needs re-platforming to UTB evidence model) and/or `EXTRACT` (take list/detail/branch fetch + token extraction modules).
- **Maintenance/stability (prior knowledge; verify):** community-maintained; keep watching it as a fast-moving adapter layer that breaks when OpenAI changes backend shape/Cloudflare behavior — treat as living upstream to track, not as frozen code.

## 2. joningi/chatgpt-export

- **Type:** Python exporter for ChatGPT conversations, notable for **branch/tree export** into multiple formats (Markdown/JSON/HTML).
- **Useful components (prior knowledge, approximate — verify):** branch-tree traversal/export logic, conversation detail parsing, format renderers.
- **Tentative classification:** `ADAPTER` / `EXTRACT` (branch/format logic); possibly `NOT USEFUL` as-is if its auth/endpoint assumptions are stale.
- **Maintenance/stability (prior knowledge; verify):** appears less actively maintained than the previous entry; treat as a source of algorithms, not a supported runtime.

## 3. nborwankar/aishell

- **Type:** interactive CLI “AI shell” for working with LLMs via API keys (OpenAI/Anthropic; shell/TUI workflows).
- **Relevance to capture:** none observed from prior knowledge — it is API-key/programmatic-LLM tooling, **not** a ChatGPT-account conversation-history client.
- **Tentative classification:** `NOT USEFUL` for UTB history capture.
- **Maintenance/stability:** n/a (verify if repurposing ideas for interpreter-style skills later — out of M0 scope).

## 4. transitive-bullshit/chatgpt-api

- **Type:** Python “free-tier” ChatGPT library using an access token (not account-wide history focus).
- **Useful components:** minimal; demonstrates token-ACQUISITION patterns and history-endpoint existence, but it is chat-turn oriented and historically fragile against Cloudflare/OpenAI changes.
- **Tentative classification:** `NOT USEFUL` as-is; at most `EXTRACT` a token-extraction hint. (Note: its main use-case — chat turn generation — is **forbidden** for UTB in any case: no private write/generation endpoints in M0.)
- **Maintenance/stability (prior knowledge):** often broken by provider changes; poor reliability signal.

## 5. acheong08/ChatGPT (`revChatGPT`)

- **Type:** Python library for ChatGPT web backend; `Access Token`/`PUID` modes.
- **Useful components:** auth/session acquisition patterns, cookie/Cloudflare interactions; some conversation-listing capability.
- **Tentative classification:** `EXTRACT` (auth patterns) at most; **not** `AS-IS` for UTB (chat endpoint orientation, write-path default, instability).
- **Maintenance/stability (prior knowledge):** historically high churn/fragility vs Cloudflare; strong signal that a **HTTP-only steady-state path still needs a browser-based auth refresh** rather than static-token persistence — this aligns with M0 hypothesis H-004, but was **not measured** in this spike.

## 6. pionxzh/chatgpt-exporter (userscript / browser extension class)

- **Type:** userscript that exports conversations from the **DOM** of the web UI (manual trigger per chat).
- **Useful components:** DOM/JSON mapping of the current UI, export formats; useful as a **manual fallback reference** or a home-PC diagnostic, not as the autonomous VPS path.
- **Tentative classification:** `NOT USEFUL` for autonomous VPS capture (requires the chat open in an interactive browser); optional `EXTRACT` of export-format mapping if M1 needs a UI-parity reference. (Also cannot be required per D-004: home PC / interactive browser must not be required.)
- **Maintenance/stability (prior knowledge):** UI-reliant; breaks on UI changes; expected.

## 7. Official ChatGPT data export (Settings → Data export / GDPR-style export zip)

- **Type:** first-party manual export containing `conversations.json` (full tree incl. branches and project membership) in a zip.
- **Useful components:** ground-truth corpus for validating M1 collector output; definition of complete tree shape; legal data-portability channel.
- **Tentative classification:** not reusable code; **reference ground truth** for acceptance testing (not part of the autonomous path).
- **Maintenance/stability:** first-party; stable but manual — unsuitable as an autonomous collector alone.

---

## Not discovered (honest note)

The contract asks to also consider “better current candidates discovered during the spike”. Because the sandbox had **no network**, no new upstream candidates could be discovered or evaluated. The coordinator should repeat this inventory on a networked runtime (e.g., GitHub search for `chatgpt export` / `chatgpt history` maintained in the last 6 months, plus checking latest stars/activity) before M1.

## Upstreams not yet examined (required for a complete inventory on the real VPS)

- Fresh GitHub search results (activity in last 12 months):
  - maintained Python/Node exporters (`chatgpt-export`-class);
  - Cloudflare-aware session/auth helpers (`cloudscraper`, `curl_cffi`-based clients);
  - official SDKs (for reference only; they do not expose web-account history).
- These remain **unexamined** and must not be treated as risk-free.

## Maintenance/stability observations (all prior-knowledge)

- Web-backend client libraries for ChatGPT are **high-churn**: OpenAI/Cloudflare changes regularly break token/cookie flows. The practical pattern in the ecosystem is: **keep a browser-based auth-refresh path, keep HTTP reads lean, and treat every endpoint as versioned/observed rather than assumed**.
- This reinforces, but does not prove, the contract’s design candidates; no M0 measurement exists yet.

## Privacy notes

No upstream code was downloaded or executed in this spike; no tokens/cookies/profiles were touched. Inspecting upstreams on the real runtime must avoid committing any captured secrets and must not print tokens (contract security constraints).