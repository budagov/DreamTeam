# Autonomous Development System — Agent Configuration

This project uses the Autonomous Development System. Roles can be executed **as subagents** (via `mcp_task`) or by loading the prompt from `.cursor/agents/`.

## Subagents (Dispatch via mcp_task)

**Full details:** `.cursor/agents/orchestrator.md`

**Main Orchestrator** (when /start or /run): ONLY dispatches **Left** or **Right**. Does NOT dispatch Developer, Planner, Reviewer, etc. — Left and Right do that.

**Left/Right** dispatch: Planner, Developer, Reviewer, DevExperiencer, Git-Ops, Learning, FixPlanner, Researcher, Meta Planner, Auditor, Terminal.

**When to dispatch:**
- **Left** — Main Orchestrator dispatches (orchestrator-left). Left runs up to 33 tasks per batch (planning or execution). Project can have thousands of tasks.
- **Right** — Main Orchestrator dispatches (orchestrator-right). Right runs up to 33 tasks per batch.
- **Planner** — Left/Right dispatch (planner). Planner breaks into epics, dispatches Sub-Planner.
- **Planner-Sub** — Planner dispatches (planner-sub), not Orchestrator
- **DevExperiencer** — Left/Right dispatch after Reviewer (dev-experiencer)
- **Learning** — Every 10 tasks, or on cyclic failure (task blocked after 2 Critical retries). Analyzes DevExperience, updates Developer, dispatches FixPlanner (learning)
- **FixPlanner** — Corrects tasks based on Learning analysis (fix-planner)
- **Developer** — Task from scheduler ready for implementation
- **Reviewer** — After each task completion (spec compliance, then code quality)
- **Git-Ops** — After Reviewer approval — git commit (ONLY Git-Ops does commits)
- **Terminal** — dreamteam commands (fallback when MCP unavailable)
- **MCP dreamteam-db** — DB tools: dreamteam_get_task, dreamteam_get_memory, dreamteam_set_memory, dreamteam_get_dag_state, dreamteam_recent_tasks
- **Researcher** — When `task_counter.py` prints `TRIGGER_RESEARCHER`
- **Meta Planner** — When `task_counter.py` prints `TRIGGER_META_PLANNER`
- **Auditor** — When `task_counter.py` prints `TRIGGER_AUDITOR`

**How to dispatch:**
- Use `mcp_task` with `subagent_type`: `developer`, `code-reviewer`, `planner`, `planner-sub`, `researcher`, `meta-planner`, `auditor`, `git-ops`, `shell` (Terminal), `orchestrator-left`, `orchestrator-right`, `dev-experiencer`, `learning`, `fix-planner`
- Git-Ops is the ONLY agent that does commits. Main Orchestrator runs NO Terminal — Left/Right do ALL Terminal work.
- For Developer: include task ID, `.dreamteam/memory/architecture.md` snippet
- For Reviewer: include changed files, task ID, architecture rules (Reviewer uses Terminal get-task for task content)

**Main Orchestrator workflow:** verify-tasks → set-goal → Dispatch Left → (Left returns BATCH_DONE) → Dispatch Right → alternate until ALL_COMPLETE.

**Left/Right workflow:** run-next → Developer → Reviewer → DevExperiencer → Git-Ops → update-task done. TRIGGER_* → Learning/Researcher/Meta Planner/Auditor.

## Agent Prompts

| Role | Prompt File | When to Use |
|------|-------------|-------------|
| Orchestrator | `.cursor/agents/orchestrator.md` | ONLY dispatches Left/Right. Left/Right do all subagent orchestration. |
| Left | `.cursor/agents/orchestrator-left.md` | Sub-orchestrator, up to 33 tasks per batch (context switch; project can have thousands) |
| Right | `.cursor/agents/orchestrator-right.md` | Sub-orchestrator, up to 33 tasks per batch |
| Planner | `.cursor/agents/planner.md` | New goal, epic, or task decomposition |
| Planner-Sub | `.cursor/agents/planner-sub.md` | Expand one epic into 15–25 subtasks |
| Developer | `.cursor/agents/developer.md` | Executing a task from scheduler |
| Reviewer | `.cursor/agents/reviewer.md` | After task completion, code review |
| Git-Ops | `.cursor/agents/git-ops.md` | Git commit (ONLY agent that does commits) |
| Terminal | `.cursor/agents/terminal.md` | dreamteam commands (no git-commit from Orchestrator) |
| Researcher | `.cursor/agents/researcher.md` | Every 20 tasks (TRIGGER_RESEARCHER) |
| Meta Planner | `.cursor/agents/meta-planner.md` | Every 50 tasks (TRIGGER_META_PLANNER) |
| Auditor | `.cursor/agents/auditor.md` | Every 200 tasks (TRIGGER_AUDITOR) |
| DevExperiencer | `.cursor/agents/dev-experiencer.md` | After each Reviewer |
| Learning | `.cursor/agents/learning.md` | Every 10 tasks (TRIGGER_LEARNING) |
| FixPlanner | `.cursor/agents/fix-planner.md` | Dispatched by Learning |

## Skills

Project skills in `.cursor/skills/`:

- `planner-task-decomposition`
- `planner-sub-expand`
- `developer-execution`
- `researcher-context-compression`
- `meta-planner-optimization`
- `auditor-system-audit`
- `reviewer-code-review`

**Superpowers (subagent workflows):**
- `subagent-driven-development` — Execute plan with subagent per task + two-stage review
- **Parallelism is FORBIDDEN** — One task, one subagent at a time

## Rules

- `.cursor/rules/autonomous-dev-system.mdc` — Always apply
- `.cursor/rules/task-execution.mdc` — When editing `.dreamteam/tasks/**/*.md`
- `.cursor/agents/orchestrator.md` — Main Orchestrator: only Left/Right. Load when /start or /run.

## Commands

Use `python -m dreamteam`. See guide/COMMANDS.md.
