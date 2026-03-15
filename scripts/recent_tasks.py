#!/usr/bin/env python3
"""List recent done tasks from DB. For Researcher context."""

import os
import sys

import project
from db_utils import get_recent_tasks


def main() -> None:
    """Output last N done tasks (id, title, content excerpt)."""
    limit = 20
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])

    if not os.path.exists(project.get_db_path()):
        print("Database not found.", file=sys.stderr)
        sys.exit(1)

    tasks = get_recent_tasks(limit)
    print("# Recent done tasks\n")
    for t in tasks:
        excerpt = (t["excerpt"] or "").replace("\n", " ") if t.get("excerpt") else ""
        print(f"## {t['id']}: {t['title']}")
        if excerpt:
            print(excerpt)
        print()


if __name__ == "__main__":
    main()
