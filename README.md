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

**Engine and project are separate.** DreamTeam folder = engine only. Your project = separate folder.

```bash
# 1. Install engine (clone + install)
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
.\setup.ps1               # or: ./setup.sh  (installs only, no project)

# 2. Create project in a CLEAN folder (not inside DreamTeam!)
cd C:\Projects\my-app     # empty folder
python -m dreamteam new-project .

# 3. Open my-app in Cursor → /start + goal → /run
```

Result: `my-app/` has only `.dreamteam/`, `.cursor/`, and your `src/` — no engine code.

## Documentation

- [INSTALL.md](INSTALL.md) — Install from clone, troubleshooting
- [Quick Start Agent](docs/QUICK_START_AGENT.md) — `/start`, `/run`, task workflow
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
