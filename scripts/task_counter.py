#!/usr/bin/env python3
"""Task counter: show tasks_completed. Increment is done by update-task done."""

import sqlite3
import os
import sys

import project
from triggers import (
    TRIGGER_RESEARCHER,
    TRIGGER_META_PLANNER,
    TRIGGER_AUDITOR,
    TRIGGER_LEARNING,
    TRIGGER_BATCH_SWITCH,
)

DB_PATH = project.get_db_path()


def get_count(cursor: sqlite3.Cursor) -> int:
    """Get current tasks_completed value."""
    cursor.execute("SELECT value FROM metrics WHERE metric = 'tasks_completed'")
    row = cursor.fetchone()
    return row[0] if row else 0


def status() -> int:
    """Print current count and total tasks."""
    if not os.path.exists(DB_PATH):
        print("Database not found. Run: python -m dreamteam init-db", file=sys.stderr)
        return 0

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        cursor = conn.cursor()
        count = get_count(cursor)
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]
    finally:
        conn.close()

    print(f"tasks_completed: {count} / {total}")
    if count > 0:
        if count % TRIGGER_RESEARCHER == 0:
            print("TRIGGER_RESEARCHER")
        if count % TRIGGER_META_PLANNER == 0:
            print("TRIGGER_META_PLANNER")
        if count % TRIGGER_AUDITOR == 0:
            print("TRIGGER_AUDITOR")
        if count % TRIGGER_LEARNING == 0:
            print("TRIGGER_LEARNING")
        if count % TRIGGER_BATCH_SWITCH == 0:
            print("TRIGGER_BATCH_SWITCH")
    return count


if __name__ == "__main__":
    status()
