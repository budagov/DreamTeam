#!/usr/bin/env python3
"""Shared DB utilities. Used by recover, run_next, etc."""

import os
import sqlite3

import project

DB_PATH = project.get_db_path()


def fix_tasks_completed_metric() -> bool:
    """Set metrics.tasks_completed = count of done tasks. Fixes drift."""
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'done'")
        actual = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO metrics (metric, value) VALUES ('tasks_completed', ?) ON CONFLICT(metric) DO UPDATE SET value = excluded.value",
            (actual,),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_recent_tasks(limit: int = 20) -> list[dict]:
    """Get last N done tasks from DB. Returns list of {id, title, excerpt}."""
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")
        has_content = any(col[1] == "content" for col in cursor.fetchall())
        if has_content:
            cursor.execute(
                "SELECT id, title, content FROM tasks WHERE status = 'done' ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            )
        else:
            cursor.execute(
                "SELECT id, title, '' FROM tasks WHERE status = 'done' ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            )
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()
    return [
        {"id": r[0], "title": r[1], "excerpt": (r[2] or "")[:500] if len(r) > 2 else ""}
        for r in rows
    ]
