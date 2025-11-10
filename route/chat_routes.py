"""
Chat API routes (/api/chat, /api/history)
"""

from flask import Blueprint, request, jsonify, session
import uuid

from database.db import (
    create_session,
    session_exists,
    add_message,
    get_messages,
    get_recent_context,
)
from service.gemini_service import get_gemini_service

chat_bp = Blueprint('chat', __name__, url_prefix='/api')


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from frontend
    POST body: { "message": "user message", "session_id": "optional" }
    Returns: { "reply": "bot response", "session_id": "session_id" }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message manquant'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Get or create session ID
        session_id = data.get('session_id') or session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        # Create DB session if needed
        if not session_exists(session_id):
            session_id = create_session()
            session['session_id'] = session_id
        
        # Persist user message
        add_message(session_id, 'user', user_message)
        
        # Generate bot response via Gemini service (no mock fallback)
        try:
            gemini_service = get_gemini_service()
            context = get_recent_context(session_id, max_messages=10)
            bot_response = gemini_service.generate_reply(user_message, context)
        except Exception as bot_error:
            print(f'[ERROR] AI generation error: {bot_error}')
            return jsonify({
                'error': 'Erreur lors de la génération de la réponse',
                'details': str(bot_error)
            }), 502
        
        # Save bot response
        add_message(session_id, 'assistant', bot_response)
        
        return jsonify({
            'reply': bot_response,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f'[ERROR] Error in /api/chat: {e}')
        return jsonify({
            'error': 'Erreur serveur interne',
            'details': str(e)
        }), 500


@chat_bp.route('/history', methods=['GET'])
def history():
    """
    Get conversation history for current session
    Returns: { "messages": [...], "session_id": "session_id" }
    """
    try:
        session_id = session.get('session_id')
        if not session_id or not session_exists(session_id):
            return jsonify({'messages': [], 'session_id': None})
        msgs = get_messages(session_id)
        return jsonify({'messages': msgs, 'session_id': session_id})
        
    except Exception as e:
        print(f'[ERROR] Error in /api/history: {e}')
        return jsonify({'error': 'Erreur lors de la récupération de l\'historique'}), 500
