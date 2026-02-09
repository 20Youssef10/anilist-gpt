"""
Authentication routes for AniList OAuth
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

from src.config.settings import settings
from src.services.auth.oauth import AniListOAuth

router = APIRouter()
oauth_service = AniListOAuth()


@router.get("/login")
async def login():
    """Redirect to AniList OAuth authorization"""
    state = "random-state-string"  # Should be generated securely
    auth_url = oauth_service.get_auth_url(state)
    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code: str = None, state: str = None, error: str = None):
    """Handle OAuth callback from AniList"""
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")

    try:
        token_data = await oauth_service.exchange_code(code)
        return {
            "status": "success",
            "message": "Authentication successful",
            "token_type": token_data.get("token_type"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token exchange failed: {str(e)}")


@router.get("/logout")
async def logout(user_id: str):
    """Logout and revoke tokens"""
    await oauth_service.revoke_tokens(user_id)
    return {"status": "success", "message": "Logged out successfully"}
