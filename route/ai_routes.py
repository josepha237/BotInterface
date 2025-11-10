"""
AI health routes
"""

from flask import Blueprint, jsonify
from service.gemini_service import get_gemini_service

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/health', methods=['GET'])
def ai_health():
    svc = get_gemini_service()
    status = svc.health_check()
    return jsonify(status)
