#!/usr/bin/env python3
"""Get DevExperience history for Learning Agent. Last N records or by task range."""

import sqlite3
import os
import sys
import json

import project
DB_PATH = project.get_dev_experience_db_path()


def get_history(limit: int = 100) -> list[dict]:
    """Get last N task experiences."""
    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT task_id, reviewer_result, time_spent_minutes, attempts_count,
                   technologies_used, approaches_used, critical_feedback, created_at
            FROM task_experience
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    finally:
        conn.close()


def get_uncompleted_task_ids() -> list[str]:
    """Get task IDs that had critical/failures (from dag.db, cross-ref with experience)."""
    import project as p
    dag_path = p.get_db_path()
    if not os.path.exists(dag_path) or not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT task_id FROM task_experience WHERE reviewer_result = 'critical'"
        )
        critical_tasks = [r[0] for r in cursor.fetchall()]
        return critical_tasks
    finally:
        conn.close()


def main() -> None:
    """Output JSON history for Learning Agent."""
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    history = get_history(limit)
    print(json.dumps(history, indent=2, default=str))


if __name__ == "__main__":
    main()
