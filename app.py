"""
BotInterface - Flask Backend Application
Serves the chat interface and handles bot API communication
"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

from database.db import init_db, close_db
from route.page_routes import page_bp
from route.chat_routes import chat_bp
from route.ai_routes import ai_bp

load_dotenv()

app = Flask(__name__, 
            static_folder='stactic',
            static_url_path='/static',
            template_folder='templates')

# Secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Init SQLite database
app.config["DB_PATH"] = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(os.getcwd(), "database", "botinterface.db"),
)

# Preinscription URL (Université de Douala)
app.config["PREINSCRIPTION_URL"] = os.environ.get(
    "PREINSCRIPTION_URL",
    "http://www.systhag-online.cm:8080/SYSTHAG-ONLINE/faces/etudiants/preInscription.xhtml",
)
init_db(app)
app.teardown_appcontext(close_db)

# Register blueprints
app.register_blueprint(page_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(ai_bp)


@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        "PREINSCRIPTION_URL": app.config.get("PREINSCRIPTION_URL"),
    }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Route non trouvée'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    print(f'[ERROR] Internal error: {error}')
    return jsonify({'error': 'Erreur serveur interne'}), 500


if __name__ == '__main__':
    # Development server
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', '5000'))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
