---
name: planner-sub-expand
description: Expands one epic into 15–25 subtasks. ONLY Planner uses this. Left/Right NEVER call planner-sub — they call planner.
---

# Sub-Planner Expand

## When to Use

- **ONLY Planner** dispatches Sub-Planner (planner-sub) per epic
- **Left and Right must NEVER call planner-sub** — they call planner. Planner then calls planner-sub.
- If you are Left or Right and need planning → call **planner** (subagent_type: planner), NOT planner-sub

## Workflow

1. Read epic description and ID range from Planner (via prompt)
2. Break epic into 15–25 small tasks (1–3 files, ~15–30 min each)
3. Create task files in `.dreamteam/tasks/` for given ID range
4. Set dependencies: first task → previous epic; within epic → prior subtasks
5. Return one line: "DONE. Created TXXX–TYYY (N tasks)."

## Rules

- Do NOT create tasks outside the given ID range
- Do NOT modify architecture.md
- Agent: `.cursor/agents/planner-sub.md`
