#!/usr/bin/env python3
"""Print current project root. Useful for debugging project resolution."""

import project

root = project.get_project_root()
print(f"Project root: {root}")
print(f"  db: {project.get_db_path()}")
print(f"  memory: {project.get_memory_dir()}")
print(f"  tasks: {project.get_tasks_dir()}")
