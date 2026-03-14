#!/usr/bin/env python3
"""Initialize or reset the Autonomous Development System SQLite database."""

import sqlite3
import os
import sys

import project
DB_PATH = project.get_db_path()


def init_db(reset: bool = False) -> None:
    """Create database and schema. If reset=True, drop existing tables first."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if reset:
        cursor.execute("DROP TABLE IF EXISTS tasks")
        cursor.execute("DROP TABLE IF EXISTS metrics")
        cursor.execute("DROP TABLE IF EXISTS context_graph")
        cursor.execute("DROP TABLE IF EXISTS vector_code")
        conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT,
            status TEXT,
            priority INTEGER,
            dependencies TEXT,
            owner TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            metric TEXT PRIMARY KEY,
            value INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS context_graph (
            module TEXT,
            functions TEXT,
            dependencies TEXT,
            embedding BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vector_code (
            path TEXT,
            chunk TEXT,
            embedding BLOB,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO metrics (metric, value) VALUES ('tasks_completed', 0)"
    )
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    reset = "--reset" in sys.argv
    init_db(reset=reset)
