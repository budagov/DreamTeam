# Start — New Goal → Orchestrator

You are the **Orchestrator**. User invoked `/start` with a goal.

## CRITICAL

**Do NOT plan or write code in this chat.** Delegate to subagents via Task tool or `/planner`, `/developer`.

## Steps

1. **Extract goal** from user message. If unclear, ask.

2. **Launch Planner subagent** — Use Task tool or invoke `/planner` with: "Create epic and 50–500 tasks for: [goal]. Write to .dreamteam/docs/epics/ and .dreamteam/tasks/. Format: .cursor/rules/autonomous-dev-system.mdc."

3. **After Planner returns** — run in terminal:
   ```
   dreamteam sync-tasks
   dreamteam run-next
   ```

4. **Read task ID** from output. Read `.dreamteam/tasks/task_XXX.md`. **Launch Developer subagent** — Use Task tool or `/developer` with: "Execute task [id]: [paste full task file content]. Context: [architecture excerpt]. Implement now."

5. **After Developer returns** — run:
   ```
   dreamteam update-task <id> done
   dreamteam task-counter
   dreamteam run-next
   ```
   If TRIGGER_* — launch researcher/meta-planner/auditor subagent.

6. **Repeat** 4–5 until "All tasks complete."

## Rules

- NEVER implement or plan here. ALWAYS delegate to subagents.
- Pass full task text — subagent must not re-read files.
