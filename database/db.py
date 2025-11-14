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

-- User table with authentication fields
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'student' CHECK(role IN ('student', 'admin', 'guest')),
    is_verified INTEGER DEFAULT 0,
    verification_token TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_email ON user(email);
CREATE INDEX IF NOT EXISTS idx_user_verification_token ON user(verification_token);

-- Session table linked to users
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    user_id INTEGER,
    status TEXT DEFAULT 'active',
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_session_uuid ON session(uuid);
CREATE INDEX IF NOT EXISTS idx_session_user_id ON session(user_id);

-- Message table
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    error TEXT,
    FOREIGN KEY(session_id) REFERENCES session(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_message_session_id ON message(session_id);

-- Password reset table
CREATE TABLE IF NOT EXISTS password_reset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TEXT NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_password_reset_token ON password_reset(token);
CREATE INDEX IF NOT EXISTS idx_password_reset_user_id ON password_reset(user_id);

-- Login attempt table for security
CREATE TABLE IF NOT EXISTS login_attempt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    ip_address TEXT,
    success INTEGER DEFAULT 0,
    attempted_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_login_attempt_email ON login_attempt(email);
CREATE INDEX IF NOT EXISTS idx_login_attempt_attempted_at ON login_attempt(attempted_at);
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
        _migrate_existing_user_table(conn)
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def _migrate_existing_user_table(conn: sqlite3.Connection) -> None:
    """Upgrade pre-auth 'user' table to include new authentication columns if missing.

    Earlier versions of the schema created a minimal `user` table without
    password_hash / role / is_verified / verification_token / updated_at.
    Because we now create indexes referencing `verification_token`, startup
    would fail with `sqlite3.OperationalError: no such column: verification_token`.

    This function inspects the existing table (if any) and issues ALTER TABLE
    statements to add the missing columns with safe defaults so constraints
    won't break. Columns added:
      - password_hash TEXT NOT NULL DEFAULT ''
      - role TEXT DEFAULT 'student'
      - is_verified INTEGER DEFAULT 0
      - verification_token TEXT (nullable)
      - updated_at TEXT DEFAULT CURRENT_TIMESTAMP

    NOTE: Existing users will have an empty password_hash and must be updated
    on next login/registration flow. If you prefer a clean slate you can delete
    the database file instead of relying on this migration logic.
    """
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    if not cur.fetchone():
        return  # Table does not exist yet; fresh create will handle it.

    cur = conn.execute("PRAGMA table_info(user)")
    existing_cols = {row[1] for row in cur.fetchall()}
    required_defs = {
        "password_hash": "ALTER TABLE user ADD COLUMN password_hash TEXT DEFAULT '' NOT NULL",
        "role": "ALTER TABLE user ADD COLUMN role TEXT DEFAULT 'student'",
        "is_verified": "ALTER TABLE user ADD COLUMN is_verified INTEGER DEFAULT 0",
        "verification_token": "ALTER TABLE user ADD COLUMN verification_token TEXT",
        "updated_at": "ALTER TABLE user ADD COLUMN updated_at TEXT DEFAULT CURRENT_TIMESTAMP",
    }
    for col, ddl in required_defs.items():
        if col not in existing_cols:
            conn.execute(ddl)
    conn.commit()


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
    "create_user",
    "get_user_by_email",
    "get_user_by_id",
    "update_user_verification",
    "create_password_reset",
    "get_password_reset",
    "mark_reset_used",
    "log_login_attempt",
]


# ---- User operations ----

def create_user(email: str, display_name: str, password_hash: str, 
                role: str = 'student', verification_token: Optional[str] = None) -> int:
    """Create a new user and return user ID"""
    db = get_db()
    cur = db.execute(
        """INSERT INTO user (email, display_name, password_hash, role, verification_token) 
           VALUES (?, ?, ?, ?, ?)""",
        (email, display_name, password_hash, role, verification_token)
    )
    db.commit()
    return cur.lastrowid


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    db = get_db()
    cur = db.execute(
        """SELECT id, email, display_name, password_hash, role, is_verified, created_at 
           FROM user WHERE email = ?""",
        (email,)
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "display_name": row[2],
        "password_hash": row[3],
        "role": row[4],
        "is_verified": bool(row[5]),
        "created_at": row[6],
    }


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    db = get_db()
    cur = db.execute(
        """SELECT id, email, display_name, role, is_verified, created_at 
           FROM user WHERE id = ?""",
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "display_name": row[2],
        "role": row[3],
        "is_verified": bool(row[4]),
        "created_at": row[5],
    }


def update_user_verification(email: str, is_verified: bool = True):
    """Mark user email as verified"""
    db = get_db()
    db.execute(
        "UPDATE user SET is_verified = ?, verification_token = NULL, updated_at = CURRENT_TIMESTAMP WHERE email = ?",
        (1 if is_verified else 0, email)
    )
    db.commit()


# ---- Password reset operations ----

def create_password_reset(user_id: int, token: str, expires_at: str) -> int:
    """Create password reset token"""
    db = get_db()
    cur = db.execute(
        "INSERT INTO password_reset (user_id, token, expires_at) VALUES (?, ?, ?)",
        (user_id, token, expires_at)
    )
    db.commit()
    return cur.lastrowid


def get_password_reset(token: str) -> Optional[Dict[str, Any]]:
    """Get password reset by token"""
    db = get_db()
    cur = db.execute(
        """SELECT id, user_id, token, expires_at, used, created_at 
           FROM password_reset WHERE token = ?""",
        (token,)
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "user_id": row[1],
        "token": row[2],
        "expires_at": row[3],
        "used": bool(row[4]),
        "created_at": row[5],
    }


def mark_reset_used(token: str):
    """Mark password reset token as used"""
    db = get_db()
    db.execute(
        "UPDATE password_reset SET used = 1 WHERE token = ?",
        (token,)
    )
    db.commit()


def update_user_password(user_id: int, password_hash: str):
    """Update user password"""
    db = get_db()
    db.execute(
        "UPDATE user SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (password_hash, user_id)
    )
    db.commit()


# ---- Login attempt operations ----

def log_login_attempt(email: str, ip_address: Optional[str], success: bool):
    """Log login attempt for security monitoring"""
    db = get_db()
    db.execute(
        "INSERT INTO login_attempt (email, ip_address, success) VALUES (?, ?, ?)",
        (email, ip_address, 1 if success else 0)
    )
    db.commit()

