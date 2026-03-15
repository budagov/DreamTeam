# DreamTeam Install

## Workflow (engine ≠ project)

DreamTeam folder = engine. Your project = separate folder. Never mix.

```powershell
# 1. Install engine (one-time)
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
.\setup.ps1   # installs only, does NOT create project here

# 2. Create project in a SEPARATE folder
cd C:\Projects\my-app
python -m dreamteam new-project .

# 3. Open my-app in Cursor, run /start + goal, dreamteam run-next
```

Result: `my-app/` contains only `.dreamteam/`, `.cursor/`, and your code. No engine files.

## Project structure

```
my-app/
├── .dreamteam/   # db, memory, tasks
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

## Vector search (Qdrant)

For 100+ tasks or large knowledge bases, install vector support:

```powershell
pip install dreamteam[vector]
```

**Default: local mode** — No Docker. Data stored in `.dreamteam/db/qdrant/`. Works out of the box.

**Optional: Qdrant server** (for shared/remote use):

```powershell
# Run Qdrant in Docker
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

# Use server
$env:QDRANT_URL = "http://localhost:6333"
python -m dreamteam vector-index
python -m dreamteam vector-search "your query"
```
