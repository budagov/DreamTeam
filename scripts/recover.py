#!/usr/bin/env python3
"""Recovery: fix DB/file sync, reset stuck tasks, validate memory."""

import os
import sys
import sqlite3
from datetime import datetime, timezone, timedelta

import project
DB_PATH = project.get_db_path()
STUCK_MINUTES = 60  # in_progress older than this -> reset to todo


def sync_tasks() -> bool:
    """Run sync_tasks.py."""
    import subprocess
    r = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "sync_tasks.py")],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        capture_output=True,
        text=True,
    )
    print(r.stdout or "")
    if r.stderr:
        print(r.stderr, file=sys.stderr)
    return r.returncode == 0


def reset_stuck_tasks(minutes: int = STUCK_MINUTES) -> list[str]:
    """Reset in_progress tasks older than minutes to todo."""
    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "SELECT id FROM tasks WHERE status = 'in_progress' AND updated_at < ?",
        (cutoff,),
    )
    stuck = [row[0] for row in cursor.fetchall()]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    for tid in stuck:
        cursor.execute("UPDATE tasks SET status = 'todo', updated_at = ? WHERE id = ?", (now, tid))
    conn.commit()
    conn.close()
    return stuck


def reset_task(task_id: str) -> bool:
    """Reset specific task from in_progress to todo."""
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE tasks SET status = 'todo', updated_at = ? WHERE id = ? AND status = 'in_progress'", (now, task_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    if affected:
        sys.path.insert(0, os.path.dirname(__file__))
        from update_task import update_task_file
        update_task_file(task_id, "todo")
    return affected > 0


def main() -> None:
    """Run recovery steps. Use: recover.py [--reset T001]"""
    if "--reset" in sys.argv:
        idx = sys.argv.index("--reset")
        if idx + 1 < len(sys.argv):
            tid = sys.argv[idx + 1]
            if reset_task(tid):
                print(f"Reset {tid} to todo.")
            else:
                print(f"Task {tid} not found or not in_progress.", file=sys.stderr)
            return
    print("Recovery: sync, reset stuck, verify")
    print("-" * 40)

    # 1. Sync files -> DB
    print("1. Syncing tasks...")
    sync_tasks()

    # 2. Reset stuck in_progress
    stuck = reset_stuck_tasks()
    if stuck:
        print(f"2. Reset stuck tasks (in_progress >{STUCK_MINUTES}min): {', '.join(stuck)}")
        # Also update task files
        sys.path.insert(0, os.path.dirname(__file__))
        from update_task import update_task_file
        for tid in stuck:
            update_task_file(tid, "todo")
    else:
        print("2. No stuck tasks.")

    # 3. Verify
    print("3. Verifying...")
    import subprocess
    r = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "verify_tasks.py")],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        capture_output=True,
        text=True,
    )
    print(r.stdout or "")
    if r.returncode != 0:
        print("Verify failed. Run sync_tasks again if needed.", file=sys.stderr)

    # 4. Check memory
    print("4. Checking memory...")
    r = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "check_memory.py")],
        cwd=os.path.dirname(os.path.dirname(__file__)),
        capture_output=True,
        text=True,
    )
    print(r.stdout or "")
    if r.returncode != 0:
        print("Memory check failed. Run Researcher to compress.", file=sys.stderr)

    print("-" * 40)
    print("Recovery done. Run: dreamteam run-next")


if __name__ == "__main__":
    main()
