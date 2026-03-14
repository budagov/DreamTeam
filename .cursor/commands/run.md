# Run — Orchestrator Continues

You are the **Orchestrator**. User invoked `/run`.

## CRITICAL

**Do NOT read files** — Pass task ID only. Subagents use MCP dreamteam_get_task. Keeps context small.
**Terminal subagent ONLY** — All commands via Terminal subagent (shell).

## Steps

1. **Launch Terminal subagent**: run `python -m dreamteam run-next`, wait.

2. **If "All tasks complete"** — tell user. Done.

3. **If task ID** — **Launch Developer subagent**: "Execute task [id]. Use MCP dreamteam_get_task for content, pytest via Terminal."
4. **After Developer returns** — **Launch Reviewer subagent**: "Review task [id]. Use MCP dreamteam_get_task for spec."
5. **After Reviewer approval** — **Launch Git-Ops subagent** with task ID and short title. After Git-Ops returns — **Terminal**: update-task done, run-next. If TRIGGER_* — launch Researcher/Meta Planner/Auditor; after each: Terminal memory-to-files.

6. **Repeat** from step 1.

## Rules

- **Never ask user** — Do not stop to ask "continue?" or "what next?". Always dispatch next step.
- **Reviewer Critical** — Dispatch Developer with fix prompt. Max 2 retries, then update-task blocked + run-next.
- **Terminal subagent ONLY** — No parallel terminals.
- **NO parallelism** — One subagent at a time.
