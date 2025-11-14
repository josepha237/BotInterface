"""
Authentication Routes Blueprint
Handles user authentication: login, register, logout, password reset
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from functools import wraps
import re

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function


def validate_email(email):
    """Validate university email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@(univ-douala\.cm|student\.univ-douala\.cm)$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength (min 8 chars, 1 uppercase, 1 lowercase, 1 number)"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, "OK"


# ==================== PAGE ROUTES ====================

@auth_bp.route('/login')
def login_page():
    """Render login page"""
    if 'user_id' in session:
        return redirect(url_for('pages.chat'))
    return render_template('login.html')


@auth_bp.route('/register')
def register_page():
    """Render registration page"""
    if 'user_id' in session:
        return redirect(url_for('pages.chat'))
    return render_template('register.html')


@auth_bp.route('/forgot-password')
def forgot_password_page():
    """Render forgot password page"""
    return render_template('forgot-password.html')


# ==================== API ROUTES ====================

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Tous les champs requis doivent être remplis'}), 400
        
        full_name = data['full_name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        matricule = data.get('matricule', '').strip()
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Adresse email universitaire invalide'}), 400
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # TODO: Check if email already exists in database
        # TODO: Hash password with bcrypt
        # TODO: Store user in database
        # TODO: Send verification email
        
        # For now, return success (will be implemented with auth_service.py)
        return jsonify({
            'message': 'Compte créé avec succès',
            'user': {
                'email': email,
                'full_name': full_name
            }
        }), 201
        
    except Exception as e:
        print(f'[ERROR] Registration error: {e}')
        return jsonify({'error': 'Erreur lors de la création du compte'}), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and create session"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember = data.get('remember', False)
        
        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        # TODO: Verify credentials with database
        # TODO: Check password hash
        # TODO: Create session token
        # TODO: Log login attempt
        
        # For now, create simple session (will be implemented with auth_service.py)
        session['user_id'] = 'temp_user_id'
        session['user_email'] = email
        session.permanent = remember
        
        return jsonify({
            'message': 'Connexion réussie',
            'user': {
                'email': email
            }
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Login error: {e}')
        return jsonify({'error': 'Erreur lors de la connexion'}), 500


@auth_bp.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout user and clear session"""
    try:
        session.clear()
        return jsonify({'message': 'Déconnexion réussie'}), 200
    except Exception as e:
        print(f'[ERROR] Logout error: {e}')
        return jsonify({'error': 'Erreur lors de la déconnexion'}), 500


@auth_bp.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email requis'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Adresse email universitaire invalide'}), 400
        
        # TODO: Check if email exists in database
        # TODO: Generate reset token
        # TODO: Send reset email
        
        # Always return success for security (don't reveal if email exists)
        return jsonify({
            'message': 'Si cette adresse existe, vous recevrez un email de réinitialisation'
        }), 200
        
    except Exception as e:
        print(f'[ERROR] Forgot password error: {e}')
        return jsonify({'error': 'Erreur lors de la demande de réinitialisation'}), 500


@auth_bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token', '')
        new_password = data.get('password', '')
        
        if not token or not new_password:
            return jsonify({'error': 'Token et mot de passe requis'}), 400
        
        # Validate password strength
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # TODO: Verify reset token
        # TODO: Hash new password
        # TODO: Update password in database
        # TODO: Invalidate reset token
        
        return jsonify({'message': 'Mot de passe réinitialisé avec succès'}), 200
        
    except Exception as e:
        print(f'[ERROR] Reset password error: {e}')
        return jsonify({'error': 'Erreur lors de la réinitialisation du mot de passe'}), 500


@auth_bp.route('/api/auth/verify-email/<token>')
def verify_email(token):
    """Verify email with token"""
    try:
        # TODO: Verify email token
        # TODO: Mark email as verified in database
        
        return redirect(url_for('auth.login_page') + '?verified=true')
        
    except Exception as e:
        print(f'[ERROR] Email verification error: {e}')
        return redirect(url_for('auth.login_page') + '?verified=false')


@auth_bp.route('/api/auth/me')
@login_required
def get_current_user():
    """Get current authenticated user info"""
    try:
        return jsonify({
            'user': {
                'id': session.get('user_id'),
                'email': session.get('user_email')
            }
        }), 200
    except Exception as e:
        print(f'[ERROR] Get user error: {e}')
        return jsonify({'error': 'Erreur lors de la récupération des informations'}), 500
