#!/usr/bin/env python3
"""Store original goal/strategy from /start. Used to verify FixPlanner changes don't deviate."""

import sys

from memory_set import set_memory


def main() -> None:
    """Store goal in memory. Usage: set_goal.py [--file path] | set_goal.py "goal text" """
    if len(sys.argv) < 2:
        print("Usage: python set_goal.py \"goal text\"  OR  python set_goal.py --file <path>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Usage: python set_goal.py --file <path>", file=sys.stderr)
            sys.exit(1)
        path = sys.argv[2]
        with open(path, encoding="utf-8") as f:
            content = f.read()
    else:
        content = " ".join(sys.argv[1:])

    if set_memory("goal", content):
        print("Goal stored in DB.")
    else:
        print("Failed to store goal.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
