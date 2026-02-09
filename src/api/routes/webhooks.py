"""
Webhook routes for external integrations
"""

from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.post("/anilist")
async def anilist_webhook(request: Request):
    """Receive webhooks from AniList (if supported)"""
    payload = await request.json()
    # Process webhook payload
    return {"status": "received"}


@router.post("/airing")
async def airing_notification(request: Request):
    """Receive airing schedule updates"""
    payload = await request.json()
    # Process airing updates
    return {"status": "processed"}
