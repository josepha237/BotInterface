"""Test error path when Gemini unavailable or fails.
Ensures 502 is returned and only user message saved (no assistant error message).
"""
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
from service import gemini_service as svc_module
from database.db import get_messages, create_session

class FailingClient:
    class models:
        @staticmethod
        def generate_content(model, contents):
            raise Exception("503 UNAVAILABLE: simulated failure")


def run_test():
    # Force failing client
    svc_module._gemini_service = None  # Reset singleton
    failing = svc_module.GeminiService()
    failing.client = FailingClient()  # Inject failing client
    svc_module._gemini_service = failing

    with app.test_client() as client:
        resp = client.post('/api/chat', json={'message': 'Test erreur'})
        assert resp.status_code == 502, f"Expected 502 got {resp.status_code}"
        data = resp.get_json()
        assert 'error' in data, 'Missing error key'
        # Ensure only user message stored
        with client.session_transaction() as sess:
            session_id = sess.get('session_id')
        if session_id:
            msgs = get_messages(session_id)
            assert len(msgs) == 1 and msgs[0]['role'] == 'user', f'Assistant error message should not be stored (found {len(msgs)} messages)'
    print('[TEST] Error path without mock fallback OK')


if __name__ == '__main__':
    run_test()
