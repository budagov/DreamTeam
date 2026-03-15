#!/usr/bin/env python3
"""Record task experience to DevExperience DB. Called by DevExperiencer after Reviewer."""

import sqlite3
import os
import sys
import json

import project
DB_PATH = project.get_dev_experience_db_path()


def record(
    task_id: str,
    reviewer_result: str,
    time_spent_minutes: int | None = None,
    attempts_count: int = 1,
    technologies_used: str | None = None,
    approaches_used: str | None = None,
    critical_feedback: str | None = None,
) -> bool:
    """Insert task experience record."""
    if not os.path.exists(DB_PATH):
        from init_dev_experience import init_dev_experience
        init_dev_experience()

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO task_experience
            (task_id, reviewer_result, time_spent_minutes, attempts_count, technologies_used, approaches_used, critical_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                reviewer_result,
                time_spent_minutes,
                attempts_count,
                technologies_used,
                approaches_used,
                critical_feedback,
            ),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def main() -> None:
    """CLI: record-dev-experience <task_id> <approved|critical> [attempts] [minutes] [tech_json] [approaches] [critical_feedback]"""
    if len(sys.argv) < 3:
        print("Usage: record_dev_experience.py <task_id> <approved|critical> [attempts] [minutes] [tech] [approaches] [feedback]",
              file=sys.stderr)
        sys.exit(1)

    task_id = sys.argv[1]
    reviewer_result = sys.argv[2].lower()
    if reviewer_result not in ("approved", "critical"):
        print("reviewer_result must be approved or critical", file=sys.stderr)
        sys.exit(1)

    attempts = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    minutes = int(sys.argv[4]) if len(sys.argv) > 4 else None
    tech = sys.argv[5] if len(sys.argv) > 5 else None
    approaches = sys.argv[6] if len(sys.argv) > 6 else None
    feedback = sys.argv[7] if len(sys.argv) > 7 else None

    record(task_id, reviewer_result, minutes, attempts, tech, approaches, feedback)
    print(f"Recorded {task_id}: {reviewer_result}")


if __name__ == "__main__":
    main()
