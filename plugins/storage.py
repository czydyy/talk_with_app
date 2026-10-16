"""Small SQLite store for the example /collect command."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "collect.sqlite3"


def _database_path() -> Path:
    return Path(os.environ.get("COLLECT_DB_PATH", str(DEFAULT_DB)))


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    path = _database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        with connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS collected_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            yield connection
    finally:
        connection.close()


def add_item(session_id: str, user_id: str, content: str) -> int:
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO collected_items (session_id, user_id, content) VALUES (?, ?, ?)",
            (session_id, user_id, content),
        )
        return int(cursor.lastrowid)


def list_items(session_id: str, limit: int = 20) -> list[tuple[int, str]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, content FROM collected_items WHERE session_id = ? "
            "ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
    return [(int(item_id), str(content)) for item_id, content in rows]
