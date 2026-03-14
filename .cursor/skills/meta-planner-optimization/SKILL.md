---
name: meta-planner-optimization
description: Analyzes technical debt, optimizes DAG, resplits tasks. Use when TRIGGER_META_PLANNER fires (every 50 tasks) or when DAG needs optimization.
---

# Meta Planner Optimization

## When to Use

- `dreamteam task-counter` outputs `TRIGGER_META_PLANNER`
- After every 50 completed tasks
- When DAG has bottlenecks or tech debt accumulates

## Workflow

1. **Analyze:** Review DAG, task distribution, tech debt
2. **Identify:** Bottlenecks, oversized tasks, missing tasks
3. **Optimize:** Resplit tasks, add refactor tasks, adjust priorities
4. **Output:** New tasks, refactor tasks, architecture change suggestions

## Output

- New task files
- Refactor tasks added to DAG
- Architecture change recommendations for Researcher

## Rules

- Do not break existing dependencies
- Refactor tasks should have clear scope
- Document rationale for changes
