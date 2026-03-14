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


def _git_pull() -> None:
    """Pull latest changes before starting a task. Skip if not a git repo or pull fails."""
    r = run(["git", "pull"], check=False)
    if r.returncode == 0:
        if r.stdout and r.stdout.strip():
            print("Git pull:", r.stdout.strip())
    else:
        err = (r.stderr or r.stdout or "").lower()
        skip = (
            "not a git repository" in err
            or "not found" in err
            or "no tracking information" in err
            or "please specify which branch" in err
        )
        if not skip:
            print("Git pull failed (continuing):", (r.stderr or r.stdout or "").strip(), file=sys.stderr)


def main() -> None:
    """One round: git pull -> verify -> [auto init-db + sync if needed] -> get task -> print instructions."""
    # 0. Update from remote before each task
    _git_pull()

    # 1. Verify consistency; if mismatch, init-db (if needed) + sync
    r = run([sys.executable, os.path.join(SCRIPTS_DIR, "verify_tasks.py")], check=False)
    if r.returncode != 0:
        db_path = project.get_db_path()
        if not os.path.exists(db_path):
            run([sys.executable, os.path.join(SCRIPTS_DIR, "init_db.py")], check=False)
        print("Syncing tasks to DB...", file=sys.stderr)
        r2 = run([sys.executable, os.path.join(SCRIPTS_DIR, "sync_tasks.py")], check=False)
        if r2.returncode != 0:
            print("FAIL: sync-tasks failed. Run: python -m dreamteam init-db", file=sys.stderr)
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
    print("2. After Reviewer approval: git commit & push:")
    print(f"   python -m dreamteam git-commit {task_id} \"<short title>\"")
    print("3. Then run:")
    print()
    print(f"   python -m dreamteam update-task {task_id} done")
    print("   python -m dreamteam task-counter")
    print("   python -m dreamteam run-next")
    print()
    print("3. If task_counter prints TRIGGER_RESEARCHER:")
    print("   python -m dreamteam task-counter -> Researcher agent -> python -m dreamteam check-memory -> vector-index")
    print()
    print("5. For new session (every ~20-50 tasks): python -m dreamteam verify-tasks first")
    print("=" * 60)


if __name__ == "__main__":
    main()
