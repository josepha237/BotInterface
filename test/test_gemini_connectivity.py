"""Gemini connectivity test script.
Run: python test/test_gemini_connectivity.py
"""
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from service.gemini_service import get_gemini_service


def main():
    svc = get_gemini_service()
    health = svc.health_check()
    print("Health:", health)
    if not health.get("available"):
        print("Service unavailable, skipping generation test.")
        return
    reply = svc.generate_reply("Test de connectivité", [])
    print("Reply:", reply)


if __name__ == "__main__":
    main()
