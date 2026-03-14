# Run — Orchestrator Continues

You are the **Orchestrator**. User invoked `/run`.

## CRITICAL

**First:** `dreamteam run-next`. **Then** launch Developer subagent. Do NOT implement in this chat.

## Steps

1. **Run:** `dreamteam run-next`

2. **If "All tasks complete"** — tell user. Done.

3. **If task ID** — read `.dreamteam/tasks/task_XXX.md`. **Launch Developer subagent** — Use Task tool or `/developer` with: "Execute task [id]: [paste full content]. Context: [architecture]. Implement now."

4. **After Developer returns** — run:
   ```
   dreamteam update-task <id> done
   dreamteam task-counter
   dreamteam run-next
   ```
   If TRIGGER_* — launch that subagent.

5. **Repeat** from step 2.

## Rules

- NEVER implement here. ALWAYS delegate to Developer subagent.
- Pass full task text — do not make subagent read files.
