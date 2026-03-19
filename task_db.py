import json
import sqlite3
from pathlib import Path
from typing import Dict, List

DB_PATH = Path("task_planner.db")


def init_db(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def fetch_tasks(columns: List[str], db_path: Path = DB_PATH) -> List[Dict[str, str]]:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT payload FROM tasks ORDER BY id ASC").fetchall()

    parsed: List[Dict[str, str]] = []
    for (payload,) in rows:
        raw = json.loads(payload)
        normalized = {column: str(raw.get(column, "")) for column in columns}
        parsed.append(normalized)
    return parsed


def save_tasks(rows: List[Dict[str, str]], db_path: Path = DB_PATH) -> None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM tasks")
        conn.executemany(
            "INSERT INTO tasks (payload) VALUES (?)",
            [(json.dumps(row),) for row in rows],
        )
        conn.commit()
