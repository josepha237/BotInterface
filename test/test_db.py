"""Basic smoke test for SQLite persistence.
Run: python test/test_db.py
"""

import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app  # ensures app + DB init
from database.db import create_session, add_message, get_messages


def run_test():
    with app.app_context():
        sid = create_session()
        add_message(sid, 'user', 'Bonjour')
        add_message(sid, 'assistant', 'Salut!')
        msgs = get_messages(sid)
        assert len(msgs) == 2, f"Expected 2 messages, got {len(msgs)}"
        assert msgs[0]['role'] == 'user'
        assert msgs[1]['role'] == 'assistant'
    print("[TEST] SQLite persistence OK")


if __name__ == "__main__":
    run_test()