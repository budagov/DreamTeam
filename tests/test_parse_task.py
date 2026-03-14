"""Tests for add_task.parse_task_file."""

import pytest

from add_task import parse_task_file


def test_parse_minimal():
    content = """id: T001
title: do something
status: todo
priority: 1
dependencies: []
"""
    r = parse_task_file(content)
    assert r is not None
    assert r["id"] == "T001"
    assert r["title"] == "do something"
    assert r["status"] == "todo"
    assert r["priority"] == 1
    assert r["dependencies"] == "[]"


def test_parse_with_dependencies():
    content = """id: T002
title: second task
status: todo
priority: 2
dependencies: [T001]
"""
    r = parse_task_file(content)
    assert r is not None
    assert r["id"] == "T002"
    assert "T001" in r["dependencies"]


def test_parse_missing_id_returns_none():
    content = """title: no id
status: todo
"""
    assert parse_task_file(content) is None


def test_parse_defaults():
    content = "id: T003"
    r = parse_task_file(content)
    assert r["title"] == ""
    assert r["status"] == "todo"
    assert r["priority"] == 1
    assert r["dependencies"] == "[]"
    assert r["owner"] == ""
