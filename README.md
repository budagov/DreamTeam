# Autonomous Development System

An autonomous development engine capable of executing **500–1000 tasks** in sequence without quality degradation.

## Architecture

```
Goal → Planner → Task DAG → Scheduler → Composer Agents → Testing → Task Counter → Triggers
```

**Triggers:**
- Every 20 tasks → Researcher (context compression)
- Every 50 tasks → Meta Planner (DAG optimization)
- Every 200 tasks → Auditor (architecture audit)

## Quick Start

```bash
# 1. Clone and setup (one time)
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
./setup.sh          # Linux/Mac
# or: .\setup.ps1   # Windows PowerShell

# 2. New project (from your folder)
cd path/to/your/project
dreamteam new-project .
dreamteam run-next
```

**Or:** `python -m dreamteam` if `dreamteam` not in PATH. See [INSTALL.md](INSTALL.md).

## First Goal

In Cursor chat: **`/start`** + your goal. Example:
```
/start Build a REST API for a todo app with auth
```
Planner creates an epic and 50–500 tasks. Then: `dreamteam run-next`.

## Documentation

- [INSTALL.md](INSTALL.md) — Install from clone, troubleshooting
- [Quick Start Agent](docs/QUICK_START_AGENT.md) — `/start` and task workflow
- [Empty Project Setup](docs/EMPTY_PROJECT_SETUP.md) — Bootstrap from empty folder in Cursor
- [Running 1000 Tasks](docs/RUNNING_1000_TASKS.md) — Resilience guide for long runs
- [Instructions](docs/INSTRUCTIONS.md) — System overview and usage
- [Commands](COMMANDS.md) — All CLI commands
- [Git Worktrees](docs/GIT_WORKTREES.md) — Parallel agent setup

## Projects

Each project has its own **db/**, **memory/**, **tasks/** — brains are isolated.

- `dreamteam new-project .` — deploy in current folder
- Project root: `DREAMTEAM_PROJECT` env, or `.dreamteam` in cwd/parents

## Project Structure

```
your-project/
  .dreamteam     — Project marker
  .cursor/       — agents, rules
  db/            — dag.db (tasks, metrics, vector_code)
  memory/        — architecture.md, summaries.md
  tasks/         — task_001.md, task_002.md, ...
  src/           — your code
```

## Development

```bash
pip install -e ".[dev]"
pytest tests
```

## Requirements

- Python 3.10+
- **Core:** stdlib only (scheduler, task_counter, etc.)
- **Optional (100+ tasks):** `pip install dreamteam[vector]` for vector memory / semantic search
