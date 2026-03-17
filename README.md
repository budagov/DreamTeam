# DreamTeam — Autonomous Development Cruiser for Cursor

[![License: PolyForm](https://img.shields.io/badge/License-PolyForm_Noncommercial-blue.svg)](LICENSE)
[![System: Cursor](https://img.shields.io/badge/Designed_for-Cursor-00AEEF.svg)](https://cursor.sh)

A long-range **Autonomous Development Cruiser** capable of executing **500–1000+ sequential tasks** without quality degradation. Built for fault tolerance, continuous learning, and multi-layered agent orchestration.

> [!IMPORTANT]
> **Orchestration Zero:** DreamTeam is designed to offload work from the main chat. Run batches of 15+ tasks with minimal supervision.

**Quick Start:**
1. `python -m dreamteam new-project .` (in an empty folder)
2. Open in Cursor → `/start` + your goal
3. Start or resume the execution loop: `/run`

---

## Pipeline: High-Performance Autonomy

The system uses a recursive orchestration loop. The **Main Orchestrator** dispatches specialized sub-orchestrators to handle batches of tasks, keeping the main context clean and stable.

```mermaid
graph TD
    Goal((Goal)) --> Planner(Planner Agent)
    Planner --> DAG{Task DAG}
    DAG --> Scheduler[Scheduler]
    
    subgraph "Execution Loop (L0 Orchestration)"
        Scheduler --> Orchestrator{Left/Right Orchestrator}
        Orchestrator --> Developer[Developer Agent]
        Developer --> Reviewer[Reviewer Agent]
        Reviewer --> DevExp[DevExperiencer]
        DevExp --> GitOps[Git-Ops]
        GitOps --> Update[update-task Done]
    end
    
    Update --> Triggers{Self-Correction Triggers}
    Triggers -->|Every 10| Learning[Learning Agent -> FixPlanner]
    Triggers -->|Every 20| Researcher[Researcher -> Context Compression]
    Triggers -->|Every 50| Meta[Meta Planner -> DAG Optimization]
    
    Learning -.-> DAG
    Researcher -.-> Memory[(Memory DB)]
    Meta -.-> DAG
    
    Update --> Next[run-next]
    Next --> Scheduler
```

---

## Under the Hood: Scalable Autonomy

The system is built to minimize "Main Chat" context overflow. Using a **Dual Sub-Orchestrator system (Left/Right)**, DreamTeam offloads execution to sub-agents, leaving the main chat lean and responsive. This architectural split allows massive task sequences to run even on non-frontier models.

### AI Sub-Agent Hierarchy — Multi-Layered Intelligence

DreamTeam uses a structured hierarchy to maintain precision across long-duration projects:

| Layer | Role | Primary Agents |
|:---:|:---|:---|
| **L0** | Orchestration | Main Orchestrator, Left/Right |
| **L1** | Planning & Evolution | Planner, Meta Planner, FixPlanner |
| **L2** | Core Execution | Developer, Reviewer, Researcher |
| **L3** | System Ops | Git-Ops, DevExperiencer, Auditor |

---

## Core Mechanisms

### Fault Tolerance — Nothing Gets Lost
The system is designed to recover from crashes, mismatches, and stuck tasks without manual intervention:
*   **run-next**: Verifies DB↔Files consistency, auto-syncs if needed, and resets stuck tasks.
*   **recover**: Full system reset, integrity verification, and memory health check.
*   **State-in-DB**: All state lives in SQLite. The Cruiser can resume after a break without losing a single bit of context.

### Learnability — The Pipeline Adapts
DreamTeam improves from production feedback instead of degrading:
*   **DevExperiencer**: Records every outcome, attempt count, and time spent.
*   **Learning Agent**: Analyzes the Experience DB to detect patterns of failure or high friction.
*   **FixPlanner**: Automatically adjusts upcoming tasks (library choices, dependency updates) to avoid recurring roadblocks.
*   **Developer Updates**: The system may augment `.cursor/agents/developer-addendum.md` with additional instructions to permanently adopt successful patterns.

### Analytics Dashboard — Monitor the Friction
Launch a minimalistic web dashboard to track your Cruiser's performance:
*   **KPIs**: Total tasks, estimated tokens, and **Friction Score** (Avg Attempts).
*   **Visualization**: Identify hallucination spikes and time-heavy tasks.
*   **Task Lineage**: Track original plans vs. tasks added during self-correction.

> **Command:** `python -m dreamteam dashboard`

---

## Documentation
- [guide/](guide/) — Full setup, commands, and best practices.
- [INSTRUCTIONS.md](guide/INSTRUCTIONS.md) — System overview.
- [COMMANDS.md](guide/COMMANDS.md) — CLI reference.

---

## License
PolyForm Noncommercial 1.0.0 — personal, educational, and non-profit use only. See [LICENSE](LICENSE).

---
<p align="center">Made with heart from BuLab</p>
