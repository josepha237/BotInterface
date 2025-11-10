"""SQLite database helper module for BotInterface.

Provides connection management and CRUD operations for users, sessions and messages
based on the ER diagram (USER, SESSION, MESSAGE).

Tables (created lazily on first import / init_db call):
  user(id,email,display_name,created_at)
  session(id,uuid,user_id,status,started_at,last_activity_at)
  message(id,session_id,role,content,created_at,error)

Notes:
  * We keep "uuid" as external public identifier for sessions instead of numeric id.
  * Timestamps stored as ISO strings (UTC) via CURRENT_TIMESTAMP for simplicity.
  * For now user management is minimal; user_id can be NULL in session.
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from typing import Optional, List, Dict, Any
from flask import g, current_app

DEFAULT_DB_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(os.getcwd(), "database", "botinterface.db"),
)

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    display_name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    user_id INTEGER,
    status TEXT DEFAULT 'active',
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    error TEXT,
    FOREIGN KEY(session_id) REFERENCES session(id)
);
"""


def get_db() -> sqlite3.Connection:
    """Return a request-scoped SQLite connection (Flask 'g')."""
    if "_db_conn" not in g:
        db_path = current_app.config.get("DB_PATH", DEFAULT_DB_PATH)
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g._db_conn = conn
    return g._db_conn  # type: ignore[attr-defined]


def close_db(e=None):  # pragma: no cover - flask teardown call
    """Close the DB connection at end of request."""
    conn = g.pop("_db_conn", None)
    if conn is not None:
        conn.close()


def init_db(app=None):
    """Initialize database schema (idempotent)."""
    # Need an app context to use current_app
    if app:
        with app.app_context():
            _create_schema()
            app.logger.info("SQLite database initialized at %s", current_app.config.get("DB_PATH", DEFAULT_DB_PATH))
    else:
        _create_schema()


def _create_schema():
    conn = sqlite3.connect(current_app.config.get("DB_PATH", DEFAULT_DB_PATH))
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


# ---- Session operations ----

def create_session(user_id: Optional[int] = None) -> str:
    """Create a new session and return its public UUID."""
    session_uuid = str(uuid.uuid4())
    db = get_db()
    db.execute(
        "INSERT INTO session (uuid, user_id) VALUES (?, ?)",
        (session_uuid, user_id)
    )
    db.commit()
    return session_uuid


def touch_session(session_uuid: str):
    """Update last_activity_at timestamp for a session."""
    db = get_db()
    db.execute(
        "UPDATE session SET last_activity_at = CURRENT_TIMESTAMP WHERE uuid = ?",
        (session_uuid,)
    )
    db.commit()


def session_exists(session_uuid: str) -> bool:
    db = get_db()
    cur = db.execute("SELECT 1 FROM session WHERE uuid = ?", (session_uuid,))
    return cur.fetchone() is not None


# ---- Message operations ----

def add_message(session_uuid: str, role: str, content: str, error: Optional[str] = None) -> Dict[str, Any]:
    """Insert a message record and return stored message dict."""
    db = get_db()
    cur = db.execute("SELECT id FROM session WHERE uuid = ?", (session_uuid,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Session not found when adding message")
    session_id = row[0]
    db.execute(
        "INSERT INTO message (session_id, role, content, error) VALUES (?, ?, ?, ?)",
        (session_id, role, content, error)
    )
    db.commit()
    # Fetch inserted message for timestamp
    m_cur = db.execute(
        "SELECT id, role, content, created_at, error FROM message WHERE rowid = last_insert_rowid()"
    )
    m_row = m_cur.fetchone()
    return {
        "id": m_row[0],
        "role": m_row[1],
        "content": m_row[2],
        "timestamp": m_row[3],
        "error": m_row[4],
    }


def get_messages(session_uuid: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    db = get_db()
    cur = db.execute("SELECT id FROM session WHERE uuid = ?", (session_uuid,))
    session_row = cur.fetchone()
    if not session_row:
        return []
    session_id = session_row[0]
    sql = "SELECT role, content, created_at, error FROM message WHERE session_id = ? ORDER BY id ASC"
    params: List[Any] = [session_id]
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    m_cur = db.execute(sql, params)
    return [
        {
            "role": r[0],
            "content": r[1],
            "timestamp": r[2],
            "error": r[3],
        }
        for r in m_cur.fetchall()
    ]


def get_recent_context(session_uuid: str, max_messages: int = 10) -> List[Dict[str, Any]]:
    msgs = get_messages(session_uuid, limit=max_messages)
    # If limit applied we already have chronological from earliest to latest; ensure we only keep last max_messages
    return msgs[-max_messages:]


__all__ = [
    "init_db",
    "get_db",
    "close_db",
    "create_session",
    "touch_session",
    "session_exists",
    "add_message",
    "get_messages",
    "get_recent_context",
]
