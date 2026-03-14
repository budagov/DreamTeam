#!/usr/bin/env python3
"""One-step orchestrator: verify, get next task, print instructions. Run this to start each task round."""

import os
import sys
import subprocess

import project
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = project.get_project_root()


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run command in project root."""
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


def main() -> None:
    """One round: verify -> [auto init-db + sync if needed] -> get task -> print instructions."""
    # 1. Verify consistency; if mismatch, init-db (if needed) + sync
    r = run([sys.executable, os.path.join(SCRIPTS_DIR, "verify_tasks.py")], check=False)
    if r.returncode != 0:
        db_path = project.get_db_path()
        if not os.path.exists(db_path):
            run([sys.executable, os.path.join(SCRIPTS_DIR, "init_db.py")], check=False)
        print("Syncing tasks to DB...", file=sys.stderr)
        r2 = run([sys.executable, os.path.join(SCRIPTS_DIR, "sync_tasks.py")], check=False)
        if r2.returncode != 0:
            print("FAIL: dreamteam sync-tasks failed. Run: dreamteam init-db", file=sys.stderr)
            sys.exit(1)

    # 2. Get next task
    r = run([sys.executable, os.path.join(SCRIPTS_DIR, "scheduler.py")])
    task_id = (r.stdout or "").strip()

    if not task_id or task_id.upper() == "NONE":
        print("All tasks complete.")
        return

    # 3. Set in progress
    run([sys.executable, os.path.join(SCRIPTS_DIR, "update_task.py"), task_id, "in_progress"])

    # 4. Print instructions
    print("=" * 60)
    print(f"NEXT TASK: {task_id}")
    print("=" * 60)
    print()
    print("1. Execute this task (use Composer with .cursor/agents/developer.md)")
    print(f"2. When done, run:")
    print()
    print(f"   dreamteam update-task {task_id} done")
    print("   dreamteam task-counter")
    print("   dreamteam run-next")
    print()
    print("3. If task_counter prints TRIGGER_RESEARCHER:")
    print("   dreamteam task-counter -> Researcher agent -> dreamteam check-memory -> vector_index")
    print()
    print("4. For new session (every ~20-50 tasks): dreamteam verify-tasks first")
    print("=" * 60)


if __name__ == "__main__":
    main()
