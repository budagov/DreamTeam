#!/usr/bin/env python3
"""Sync tasks from .dreamteam/tasks/ folder to database."""

import os
import sys
import sqlite3

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(__file__))
from add_task import parse_task_file, add_task_to_cursor

import project
TASKS_DIR = project.get_tasks_dir()
DB_PATH = project.get_db_path()


def main() -> None:
    """Sync all task files to database. Tasks without files -> deprecated."""
    if not os.path.exists(TASKS_DIR):
        print("Tasks directory not found.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    count = 0
    file_ids = set()
    try:
        for name in sorted(os.listdir(TASKS_DIR)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(TASKS_DIR, name)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            task_data = parse_task_file(content)
            if task_data:
                task_data["content"] = content
                add_task_to_cursor(cursor, task_data)
                file_ids.add(task_data["id"])
                count += 1
                print(f"Synced {task_data['id']}")

        cursor.execute("SELECT id FROM tasks")
        db_ids = {r[0] for r in cursor.fetchall()}
        orphan_ids = db_ids - file_ids
        if orphan_ids:
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            for oid in orphan_ids:
                cursor.execute(
                    "UPDATE tasks SET status = 'deprecated', updated_at = ? WHERE id = ?",
                    (now, oid),
                )
                print(f"Deprecated (no file): {oid}")
            cursor.execute(
                "UPDATE metrics SET value = (SELECT COUNT(*) FROM tasks WHERE status = 'done') WHERE metric = 'tasks_completed'"
            )
        conn.commit()
    finally:
        conn.close()

    print(f"Synced {count} tasks.")


if __name__ == "__main__":
    main()
