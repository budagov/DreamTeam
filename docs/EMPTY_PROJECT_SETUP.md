# Empty Project Setup — DreamTeam in Cursor

## Scenario

You have an **empty folder** and want to use DreamTeam. How does the AI know to use dreamteam commands?

## Option A: Bootstrap first (recommended)

1. Create empty folder
2. Open terminal, `cd` into the folder
3. Run: `dreamteam bootstrap`
4. Open folder in Cursor
5. First message: **"Deploy DreamTeam"** or **"Set up the project"**
6. AI reads `.cursorrules`, runs `dreamteam new-project .`
7. Done — AI uses dreamteam commands from now on

## Option B: First message only

1. Create empty folder
2. Open in Cursor
3. Paste this as first message:

```
Deploy DreamTeam autonomous development environment.
Run: dreamteam new-project .
```

4. AI runs the command
5. Project deployed — .cursor/ rules tell AI to use dreamteam

## Prerequisites

- `pip install dreamteam` (or `pip install -e .` from DreamTeam repo)
- `dreamteam` must be in PATH (or use `python -m dreamteam`)

## After deploy

The AI will use:
- `dreamteam run-next`
- `dreamteam update-task <id> done`
- `dreamteam task-counter`
- etc.

All rules in `.cursor/rules/` and agents in `.cursor/agents/` reference dreamteam CLI.
