#!/usr/bin/env python3
"""Auditor: prepare context for Auditor agent. Run when TRIGGER_AUDITOR fires."""

import os
import sys

import project
MEMORY_DIR = project.get_memory_dir()
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")


def main() -> None:
    """Output context paths for Auditor agent."""
    arch_path = os.path.join(MEMORY_DIR, "architecture.md")
    sum_path = os.path.join(MEMORY_DIR, "summaries.md")

    print("# Auditor context\n")
    print("## Paths to analyze")
    print(f"- Architecture: {arch_path}")
    print(f"- Summaries: {sum_path}")
    print(f"- Project root: {PROJECT_ROOT}")
    print("\n## Checks to perform")
    print("- Duplicate functions across modules")
    print("- Circular dependencies in code and DAG")
    print("- Layer violations (e.g. UI depending on DB directly)")
    print("- Orphaned or dead code")
    print("\n## Output")
    print("- Audit report (markdown)")
    print("- Refactor tasks for critical issues")
    print("- Update memory/architecture.md with findings")


if __name__ == "__main__":
    main()
