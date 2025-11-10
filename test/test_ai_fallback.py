import os
import sys
from types import SimpleNamespace

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import app as app_module
from app import app

class OverloadedClient:
    class models:
        @staticmethod
        def generate_content(model, contents):
            raise Exception("503 UNAVAILABLE: The model is overloaded. Please try again later.")


def run_test():
    # Patch gemini client and config for fast retry
    app_module.gemini_client = OverloadedClient()
    app_module.GEMINI_MAX_RETRIES = 1
    app_module.GEMINI_RETRY_DELAY_MS = 10

    with app.test_client() as client:
        resp = client.post('/api/chat', json={'message': 'Bonjour'})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.data}"
        data = resp.get_json()
        assert 'réponse de secours' in data['reply'], 'Should include degraded mode note'
    print('[TEST] Gemini overload fallback OK')


if __name__ == '__main__':
    run_test()
