"""Shared DB operations for MCP tools. Resolves project root and delegates to scripts."""

import os
import sys

# Add scripts to path so we can import project and script modules
_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import project  # noqa: E402

TASKS_DIR = project.get_tasks_dir
MEMORY_DIR = project.get_memory_dir
get_project_root = project.get_project_root


def get_task(task_id: str) -> str | None:
    """Get task content from DB or file fallback."""
    from get_task import get_task as _get
    return _get(task_id)


def get_memory(key: str) -> str | None:
    """Get memory (summaries|architecture) from DB."""
    from memory_get import get_memory as _get
    return _get(key)


def set_memory(key: str, content: str) -> bool:
    """Set memory in DB."""
    from memory_set import set_memory as _set
    return _set(key, content)


def get_dag_state() -> dict:
    """Get full DAG state (tasks, metrics) from DB."""
    from meta_planner import get_dag_state as _get
    return _get()


def get_recent_tasks(limit: int = 20) -> list[dict]:
    """Get last N done tasks from DB."""
    from db_utils import get_recent_tasks as _get
    return _get(limit)
