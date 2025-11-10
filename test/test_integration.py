"""
Integration test for modularized application
Tests that blueprints and Gemini service work correctly
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app


def test_landing_page():
    """Test landing page route."""
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        assert b'Bot4Univ' in resp.data or b'bot' in resp.data.lower()
    print('[PASS] Landing page OK')


def test_app_page():
    """Test chat app page route."""
    with app.test_client() as client:
        resp = client.get('/app')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    print('[PASS] App page OK')


def test_chat_api():
    """Test chat API with mock response."""
    with app.test_client() as client:
        resp = client.post('/api/chat', json={'message': 'Bonjour'})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.get_json()
        assert 'reply' in data, 'Missing reply in response'
        assert 'session_id' in data, 'Missing session_id in response'
        assert len(data['reply']) > 0, 'Empty reply'
    print('[PASS] Chat API OK')


def test_history_api():
    """Test history API."""
    with app.test_client() as client:
        # First send a message to create session
        resp1 = client.post('/api/chat', json={'message': 'Test'})
        assert resp1.status_code == 200
        
        # Then fetch history
        resp2 = client.get('/api/history')
        assert resp2.status_code == 200
        data = resp2.get_json()
        assert 'messages' in data
        assert len(data['messages']) >= 2, 'Should have user + assistant messages'
    print('[PASS] History API OK')


def run_all_tests():
    print('\n=== Running Integration Tests ===\n')
    test_landing_page()
    test_app_page()
    test_chat_api()
    test_history_api()
    print('\n[SUCCESS] All integration tests passed ✓\n')


if __name__ == '__main__':
    run_all_tests()
