# Orchestrator — Single Process
 
```mermaid
flowchart TB
    GL(["🏷️ GitLab Issue<br/>Label Change"])
    WH["📥 Webhook Handler<br/>FastAPI :8080"]
    RULE{{"🔍 Label mapped?<br/>Label changed?"}}
    DROP(["🚫 Ignored / No-op"])
    Q[["📦 queue.Queue<br/>in-memory FIFO"]]
    W["⚙️ Worker Thread<br/>one job at a time"]
    LOAD["📖 Load skill context<br/>Ready · Plan · Build · Test · Deploy · Operate"]
    WORK["✍️ Run skill work<br/>against issue context"]
    PUSH["🌿 Push to stage branch<br/><i>stage/issue-&lt;id&gt;</i>"]
    UPD["💬 Update GitLab issue<br/>comment + stage status"]
    STATE[("💾 State Dict<br/>issue_id → last_label")]
 
    GL ==>|"webhook POST"| WH
    WH ==> RULE
    RULE -.->|"no"| DROP
    RULE ==>|"yes"| Q
    Q ==>|"dequeue in order"| W
    W ==>|"spawn"| LOAD
    LOAD ==>|"resolve label → skill"| WORK
    WORK ==> PUSH
    PUSH ==> UPD
    UPD ==>|"GitLab MCP"| GL
    UPD -.->|"on success"| STATE
    STATE -.->|"checked by"| RULE
 
    classDef trigger fill:#fce8e6,stroke:#d33,stroke-width:2px
    classDef process fill:#e8f0fe,stroke:#4285f4,stroke-width:2px
    classDef decision fill:#fef7e0,stroke:#f9ab00,stroke-width:2px
    classDef store fill:#e6f4ea,stroke:#34a853,stroke-width:2px
    classDef terminal fill:#f1f3f4,stroke:#5f6368,stroke-width:1px,stroke-dasharray: 4 3
 
    class GL trigger
    class WH,W,LOAD,WORK,PUSH,UPD process
    class RULE decision
    class Q,STATE store
    class DROP terminal
```
 
**What's in the CLI stage now:**
- **Load skill context** — resolves the current label to its skill config (from `SKILL_MAP`) and loads that skill's context/prompt. One node, six possible skills behind it (Ready, Plan, Build, Test, Deploy, Operate) — which one loads depends on the label, same as your `SKILL_MAP` lookup in code
- **Push to stage branch** — commits land on a branch named by convention, e.g. `plan/issue-123`, `build/issue-123`, so stages don't clobber each other's work
- **Update GitLab issue** — CLI posts a comment (what it did, links to branch/MR) and updates the issue via GitLab MCP, closing the loop back to the board
**Reading the arrows:**
- **Thick colored (`==>`)** — the main execution path, one event flowing end to end
- **Dotted (`-.->`)** — background links: the "no" branch, and state write/read for dedupe
**Flow:**
1. Webhook lands, gets parsed into an `IssueEvent`
2. Checked against `SKILL_MAP` (known label?) and `IssueState` (label actually changed?)
3. If both pass → pushed onto `queue.Queue` (guarantees FIFO order)
4. Single worker thread pulls jobs one at a time → never two CLI runs in parallel
5. State dict only updates **after** a successful run, so a failed job naturally retries next time that label re-fires
**All in one process** — no Redis, no message broker, no DB. State lives in memory and resets on restart (fine unless you need it to survive crashes — if you do later, just flush the dict to a JSON file on `mark_done()`).
 
**Still loosely coupled** where it matters: `SKILL_MAP` is the only thing you touch to add a new label/skill — the queue, state tracking, and worker logic don't change.
 
**Portability**: it's one file + `copilot` CLI as a dependency → drop it in a Dockerfile as-is, runs anywhere.
