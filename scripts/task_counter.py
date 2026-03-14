#!/usr/bin/env python3
"""Task counter: increment completed count and emit triggers for Researcher, Meta Planner, Auditor."""

import sqlite3
import os
import sys

import project
DB_PATH = project.get_db_path()

TRIGGER_RESEARCHER = 20
TRIGGER_META_PLANNER = 50
TRIGGER_AUDITOR = 200


def get_count(cursor: sqlite3.Cursor) -> int:
    """Get current tasks_completed value."""
    cursor.execute("SELECT value FROM metrics WHERE metric = 'tasks_completed'")
    row = cursor.fetchone()
    return row[0] if row else 0


def increment() -> int:
    """Increment tasks_completed and return new value. Emit triggers to stdout."""
    if not os.path.exists(DB_PATH):
        print("Database not found. Run: dreamteam init-db", file=sys.stderr)
        return 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE metrics SET value = value + 1 WHERE metric = 'tasks_completed'"
    )
    conn.commit()

    count = get_count(cursor)
    conn.close()

    if count % TRIGGER_RESEARCHER == 0 and count > 0:
        print("TRIGGER_RESEARCHER")
    if count % TRIGGER_META_PLANNER == 0 and count > 0:
        print("TRIGGER_META_PLANNER")
    if count % TRIGGER_AUDITOR == 0 and count > 0:
        print("TRIGGER_AUDITOR")

    return count


def status() -> int:
    """Print current count without incrementing."""
    if not os.path.exists(DB_PATH):
        print("Database not found. Run: dreamteam init-db", file=sys.stderr)
        return 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    count = get_count(cursor)
    conn.close()

    print(f"tasks_completed: {count}")
    return count


if __name__ == "__main__":
    if "--status" in sys.argv:
        status()
    else:
        count = increment()
        print(f"tasks_completed: {count}")
