from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    workflow TEXT NOT NULL,
                    redacted_input TEXT NOT NULL,
                    output TEXT NOT NULL,
                    evidence_json TEXT NOT NULL,
                    confidence TEXT NOT NULL
                )
            """)

    def save(self, workflow: str, redacted_input: str, output: str, evidence: list[dict], confidence: str) -> int:
        with self.connect() as db:
            cursor = db.execute(
                "INSERT INTO analyses(workflow, redacted_input, output, evidence_json, confidence) VALUES (?, ?, ?, ?, ?)",
                (workflow, redacted_input, output, json.dumps(evidence), confidence),
            )
            return int(cursor.lastrowid)

    def recent(self, limit: int = 20) -> list[dict]:
        with self.connect() as db:
            rows = db.execute(
                "SELECT id, created_at, workflow, output, confidence FROM analyses ORDER BY id DESC LIMIT ?",
                (min(max(limit, 1), 100),),
            ).fetchall()
        return [dict(row) for row in rows]

