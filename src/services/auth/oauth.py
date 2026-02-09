"""
AniList OAuth authentication service
"""

import httpx
import json
from datetime import datetime, timedelta
from typing import Optional, Dict

from src.config.settings import settings
from src.services.cache.redis_client import RedisClient


class AniListOAuth:
    """AniList OAuth2 implementation"""

    AUTH_URL = "https://anilist.co/api/v2/oauth/authorize"
    TOKEN_URL = "https://anilist.co/api/v2/oauth/token"

    def __init__(self):
        self.client_id = settings.ANILIST_CLIENT_ID
        self.client_secret = settings.ANILIST_CLIENT_SECRET
        self.redirect_uri = settings.ANILIST_REDIRECT_URI
        self.redis = RedisClient()

    def get_auth_url(self, state: str) -> str:
        """Generate AniList OAuth authorization URL"""
        return (
            f"{self.AUTH_URL}?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"response_type=code&"
            f"state={state}"
        )

    async def exchange_code(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                json={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "code": code,
                },
            )
            response.raise_for_status()
            data = response.json()

            # Calculate expiration
            expires_at = datetime.now() + timedelta(seconds=data["expires_in"])
            data["expires_at"] = expires_at.isoformat()

            # Store tokens
            await self._store_tokens(data)

            return data

    async def _store_tokens(self, token_data: Dict):
        """Store tokens securely"""
        # Extract user ID from access token
        user_id = await self._get_user_id_from_token(token_data["access_token"])

        key = f"oauth:tokens:{user_id}"
        await self.redis.connect()
        await self.redis.set(key, token_data, ttl=token_data["expires_in"])
        await self.redis.disconnect()

    async def _get_user_id_from_token(self, access_token: str) -> str:
        """Get user ID from access token"""
        # Query AniList for current user
        query = """
        query {
            Viewer {
                id
                name
            }
        }
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://graphql.anilist.co",
                json={"query": query},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            data = response.json()
            return str(data.get("data", {}).get("Viewer", {}).get("id", "unknown"))

    async def refresh_access_token(self, user_id: str) -> Optional[str]:
        """Refresh expired access token"""
        key = f"oauth:tokens:{user_id}"

        await self.redis.connect()
        try:
            encrypted = await self.redis.get(key)
            if not encrypted:
                return None

            token_data = (
                encrypted if isinstance(encrypted, dict) else json.loads(encrypted)
            )
            refresh_token = token_data.get("refresh_token")

            if not refresh_token:
                return None

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.TOKEN_URL,
                    json={
                        "grant_type": "refresh_token",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "refresh_token": refresh_token,
                    },
                )

                if response.status_code == 200:
                    new_data = response.json()
                    await self._store_tokens(new_data)
                    return new_data["access_token"]

                return None
        finally:
            await self.redis.disconnect()

    async def revoke_tokens(self, user_id: str):
        """Revoke and delete user tokens"""
        key = f"oauth:tokens:{user_id}"
        await self.redis.connect()
        await self.redis.delete(key)
        await self.redis.disconnect()
