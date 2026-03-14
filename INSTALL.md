# DreamTeam Install

## Clean project (standard workflow)

Engine is a library. Project folder stays minimal.

```powershell
# 1. Install DreamTeam (one-time)
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
pip install -e .
# or: .\setup.ps1   # also creates project in DreamTeam folder (for quick try)

# 2. Create project in a clean folder
cd C:\Projects\my-app
dreamteam new-project .

# 3. Open my-app in Cursor, run /start + goal, dreamteam run-next
```

Result: `my-app/` contains only `.dreamteam/`, `.cursor/`, and your code. No engine files.

## Project structure

```
my-app/
├── .dreamteam/   # db, memory, tasks, docs
├── .cursor/      # agents, rules
└── src/          # your code
```

## dreamteam not found

```
No module named dreamteam
```

Run `pip install -e .` from DreamTeam folder.

## Without install

Run from DreamTeam folder:

```powershell
cd C:\Projects\DreamTeam
python -m dreamteam new-project C:\Projects\my-project
```

Then set `DREAMTEAM_PROJECT` when working from another folder:

```powershell
$env:DREAMTEAM_PROJECT = "C:\Projects\my-project"
python -m dreamteam run-next
```
