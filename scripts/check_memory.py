#!/usr/bin/env python3
"""Validate memory files stay within bounds for 1000-task scaling."""

import os
import sys

import project
MEMORY_DIR = project.get_memory_dir()
SUMMARIES_MAX_LINES = 150
ARCHITECTURE_MAX_LINES = 200


def check_summaries() -> tuple[bool, int, str]:
    """Return (ok, line_count, message)."""
    path = os.path.join(MEMORY_DIR, "summaries.md")
    if not os.path.exists(path):
        return True, 0, "summaries.md not found (ok for new project)"

    with open(path, encoding="utf-8") as f:
        lines = len(f.readlines())

    if lines > SUMMARIES_MAX_LINES:
        return False, lines, f"summaries.md has {lines} lines (max {SUMMARIES_MAX_LINES}). Researcher must compress."
    return True, lines, f"summaries.md: {lines} lines (ok)"


def check_architecture() -> tuple[bool, int, str]:
    """Return (ok, line_count, message)."""
    path = os.path.join(MEMORY_DIR, "architecture.md")
    if not os.path.exists(path):
        return True, 0, "architecture.md not found"

    with open(path, encoding="utf-8") as f:
        lines = len(f.readlines())

    if lines > ARCHITECTURE_MAX_LINES:
        return False, lines, f"architecture.md has {lines} lines (max {ARCHITECTURE_MAX_LINES}). Consider splitting."
    return True, lines, f"architecture.md: {lines} lines (ok)"


def main() -> None:
    """Validate memory files."""
    summaries_ok, sum_lines, sum_msg = check_summaries()
    arch_ok, arch_lines, arch_msg = check_architecture()

    print(sum_msg)
    print(arch_msg)

    if not summaries_ok:
        print("\nWARNING: summaries.md exceeds limit. Run Researcher with compression rules.", file=sys.stderr)
        sys.exit(1)
    if not arch_ok:
        print("\nWARNING: architecture.md exceeds limit.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
