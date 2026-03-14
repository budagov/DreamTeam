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

**Clean project (recommended):** engine as library, project folder stays minimal.

```bash
# 1. Install DreamTeam once (clone + install)
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
pip install -e .          # or: .\setup.ps1  /  ./setup.sh

# 2. Create your project in a clean folder
cd C:\Projects\my-app     # empty folder
dreamteam new-project .

# 3. Open my-app in Cursor → /start + goal → dreamteam run-next
```

Result: `my-app/` has only `.dreamteam/`, `.cursor/`, and your `src/` — no engine code in the project.

**Quick try:** run `.\setup.ps1` inside DreamTeam folder to use it as both engine and project (for testing only).

## Documentation

- [INSTALL.md](INSTALL.md) — Install from clone, troubleshooting
- [Quick Start Agent](docs/QUICK_START_AGENT.md) — `/start` and task workflow
- [Empty Project Setup](docs/EMPTY_PROJECT_SETUP.md) — Bootstrap from empty folder in Cursor
- [Running 1000 Tasks](docs/RUNNING_1000_TASKS.md) — Resilience guide for long runs
- [Instructions](docs/INSTRUCTIONS.md) — System overview and usage
- [Commands](COMMANDS.md) — All CLI commands
- [Git Worktrees](docs/GIT_WORKTREES.md) — Parallel agent setup

## Projects

Each project has its own **`.dreamteam/`** (db, memory, tasks) — brains are isolated.

- `dreamteam new-project .` — deploy in current folder
- Project root: `DREAMTEAM_PROJECT` env, or `.dreamteam` in cwd/parents

## Project Structure

```
your-project/
  .dreamteam/    — project data (db, memory, tasks, docs)
  .cursor/       — agents, rules
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
