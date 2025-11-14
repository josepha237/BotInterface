"""
Authentication Service
Handles password hashing, JWT tokens, email validation
"""

import bcrypt
import secrets
from datetime import datetime, timedelta
import hashlib


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            print(f'[ERROR] Password verification failed: {e}')
            return False
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_verification_token(email: str) -> str:
        """Generate email verification token"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{email}:{timestamp}:{secrets.token_hex(16)}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_reset_token(email: str) -> tuple[str, datetime]:
        """Generate password reset token with expiration"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        return token, expires_at
    
    @staticmethod
    def is_token_expired(expires_at: datetime) -> bool:
        """Check if token has expired"""
        return datetime.utcnow() > expires_at
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize and normalize email"""
        return email.strip().lower()
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID"""
        return secrets.token_urlsafe(32)


# For future JWT implementation
class JWTService:
    """Service for JWT token operations (for future use)"""
    
    @staticmethod
    def create_token(user_id: str, expiration_hours: int = 24) -> str:
        """Create JWT token"""
        # TODO: Implement with PyJWT library
        # payload = {
        #     'user_id': user_id,
        #     'exp': datetime.utcnow() + timedelta(hours=expiration_hours)
        # }
        # return jwt.encode(payload, secret_key, algorithm='HS256')
        pass
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        # TODO: Implement with PyJWT library
        # return jwt.decode(token, secret_key, algorithms=['HS256'])
        pass
