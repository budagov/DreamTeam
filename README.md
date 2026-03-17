# DreamTeam — Autonomous Development Cruiser for Cursor

[![License: PolyForm](https://img.shields.io/badge/License-PolyForm_Noncommercial-blue.svg)](LICENSE)
[![System: Cursor](https://img.shields.io/badge/Designed_for-Cursor-00AEEF.svg)](https://cursor.sh)

A long-range **Autonomous Development Cruiser for Cursor** capable of executing **500–1000+ sequential tasks** without quality degradation. Built for fault tolerance, continuous learning, and multi-layered agent orchestration.

> [!IMPORTANT]
> **Orchestration Zero:** DreamTeam is designed to offload work from the main chat. It dispatches **Left and Right Sub-Orchestrators** to run batches of 15+ tasks with minimal supervision.

**Quick Start:**
1. `python -m dreamteam new-project .` (in an empty folder)
2. Open in Cursor → `/start` + your goal
3. Start or resume the execution loop: `/run`

---

## Pipeline: High-Performance Autonomy

The system uses a recursive orchestration loop. The **Main Orchestrator** dispatches specialized sub-orchestrators to handle batches of tasks, keeping the main context clean and stable.

```mermaid
graph LR
    %% Node Styling
    classDef main fill:#4f46e5,color:#fff,stroke:#3730a3,stroke-width:2px,rx:6
    classDef sub fill:#f1f5f9,stroke:#64748b,stroke-width:2px,stroke-dasharray: 5,rx:6
    classDef logic fill:#fff,stroke:#e2e8f0,stroke-width:1px,rx:4
    classDef maintain fill:#f0fdf4,stroke:#16a34a,color:#166534,rx:4
    classDef infra fill:#1e293b,color:#fff,stroke:#0f172a,rx:2
    classDef data fill:#fff,stroke:#475569,stroke-width:2px,shape:cylinder

    %% Main Flow
    Start([Goal]) --> Main[Main Orchestrator]:::main

    subgraph Strategy ["Strategic Control"]
        Main <--> Switch{Context Switching}:::sub
        Switch --- Left[Left Sub-Agent]:::sub
        Switch --- Right[Right Sub-Agent]:::sub
    end

    Left & Right --> Ops

    subgraph Ops ["Autonomous Operations"]
        direction TB
        
        subgraph Planning ["Mission Planning"]
            P1[Planner]:::logic --> P2[Sub-Planner]:::logic
        end

        subgraph Execution ["Execution Loop"]
            E1[Developer]:::logic --> E2[Reviewer]:::logic
            E2 --> E3[DevExperience]:::logic
            E3 --> E4[Git-Ops]:::logic
            E4 --> E5[update-task]:::logic
        end

        subgraph Maintenance ["Maintenance & Learning"]
            M1[Learning Agent]:::maintain --> M2[FixPlanner]:::maintain
            M3[Researcher]:::maintain
        end
    end

    %% Infrastructure & Data
    Ops -.- Term{{Terminal Subagent}}:::infra
    
    P2 --> DAG[(Task DAG)]:::data
    E5 -->|Trigger| M1
    M2 -.->|Re-Plan| DAG
    M3 -.->|Compress| MEM[(Memory DB)]:::data
    E5 -.->|Next Task| E1
```

---

## Under the Hood: Scalable Autonomy

The system is built to minimize "Main Chat" context overflow. Using a **Dual Sub-Orchestrator system (Left/Right)**, DreamTeam offloads execution to sub-agents, leaving the main chat lean and responsive. This architectural split allows massive task sequences to run even on non-frontier models.
## AI Sub-Agent Hierarchy

DreamTeam uses a multi-layered intelligence system to ensure stability over long durations:

1.  **Level 1: Cruiser Control (Main Orchestrator)**: The entry point. It doesn't perform tasks but manages the switching between "Left" and "Right" sub-orchestrators. This ensures that even for 1000-task journeys, the main chat context remains lean and responsive.
2.  **Level 2: Mission Dispatch (Sub-Orchestrators)**: Specialized dispatchers that run inside a fresh context. They decide whether to launch the **Planning Phase** or the **Execution Loop** and handle all self-correction triggers.
3.  **Level 3: Specialized Workers**: 
    *   **Planner & Sub-Planner**: Decompose high-level goals into a detailed task DAG.
    *   **Developer**: Implements features and runs tests.
    *   **Reviewer**: Verifies code quality and architectural compliance.
    *   **Git-Ops**: Handles commits and repository maintenance.
    *   **Maintenance Agents**: (Researcher, Learning, Meta-Planner, Auditor) Keep the context compressed and the pipeline optimized.

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
<p align="center">Crafted for Cursor adepts with love from <b>BuLab</b></p>
