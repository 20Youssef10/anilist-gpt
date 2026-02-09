"""
JWT token management
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

from src.config.settings import settings


class JWTManager:
    """JWT token manager"""

    def __init__(self):
        self.secret = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expiration_hours = settings.JWT_EXPIRATION_HOURS

    def create_token(self, user_id: str, data: Dict = None) -> str:
        """Create JWT token"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=self.expiration_hours),
            "iat": datetime.utcnow(),
        }

        if data:
            payload.update(data)

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh a valid token"""
        payload = self.verify_token(token)
        if payload:
            # Remove expiration and create new token
            del payload["exp"]
            del payload["iat"]
            return self.create_token(payload["user_id"], payload)
        return None
