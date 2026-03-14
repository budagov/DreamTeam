# Start — New Goal → Orchestrator

You are the **Orchestrator**. User invoked `/start` with a goal.

## CRITICAL

**Do NOT plan or write code in this chat.** Delegate to subagents via Task tool or `/planner`, `/developer`.

**Use `python -m dreamteam`** — works without PATH. Do NOT check CLI availability.

## Steps

1. **Extract goal** from user message. If unclear, ask.

2. **Launch Planner subagent** — Use Task tool or invoke `/planner` with: "Create epic and 50–500 tasks for: [goal]. Write to .dreamteam/docs/epics/ and .dreamteam/tasks/. Format: .cursor/rules/autonomous-dev-system.mdc."

3. **After Planner returns** — run in terminal:
   ```
   python -m dreamteam sync-tasks
   python -m dreamteam run-next
   ```

4. **Read task ID** from output. Read `.dreamteam/tasks/task_XXX.md`. **Launch Developer subagent** — Use Task tool or `/developer` with: "Execute task [id]: [paste full task file content]. Context: [architecture excerpt]. Implement now."

5. **After Developer returns** — **Launch Reviewer subagent** (code-reviewer) with changed files, task requirements, architecture. Use Task tool or `/code-reviewer`.

6. **After Reviewer approval** — run:
   ```
   python -m dreamteam update-task <id> done
   python -m dreamteam task-counter
   python -m dreamteam run-next
   ```
   If task_counter prints **TRIGGER_RESEARCHER** — launch researcher subagent, then `python -m dreamteam vector-index` and `python -m dreamteam check-memory`.
   If **TRIGGER_META_PLANNER** — launch meta-planner subagent.
   If **TRIGGER_AUDITOR** — launch auditor subagent.

7. **Repeat** 4–6 until "All tasks complete."

## Rules

- NEVER implement or plan here. ALWAYS delegate to subagents.
- Pass full task text — subagent must not re-read files.
