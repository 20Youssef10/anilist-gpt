"""
User list and authentication tools
"""

from typing import Dict, Any, Optional

from src.tools.registry import registry, MCPTool
from src.services.anilist.client import AniListClient
from src.services.cache.cache_service import CacheService


async def get_user_list_handler(
    user_id: Optional[int] = None,
    user_name: Optional[str] = None,
    list_type: str = "ANIME",
    status: Optional[str] = None,
    sort: str = "UPDATED_TIME",
    page: int = 1,
    per_page: int = 50,
) -> Dict[str, Any]:
    """Get a user's anime/manga list from AniList"""
    cache = CacheService()
    anilist = AniListClient()

    if not user_id and not user_name:
        return {"error": "Either user_id or user_name must be provided"}

    cache_key = f"user_list:{user_id or user_name}:{list_type}:{status or 'all'}:{page}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    variables = {"userId": user_id, "userName": user_name, "type": list_type}

    result = await anilist.get_user_list(variables)

    lists = result.get("MediaListCollection", {}).get("lists", [])

    # Filter by status if specified
    if status:
        lists = [l for l in lists if l.get("status") == status]

    formatted = {
        "user": result.get("MediaListCollection", {}).get("user", {}),
        "lists": lists,
        "total_entries": sum(len(l.get("entries", [])) for l in lists),
    }

    await cache.set(cache_key, formatted, ttl=300)  # 5 minutes

    return formatted


async def get_anime_recommendations_handler(
    reference_anime_id: Optional[int] = None,
    reference_title: Optional[str] = None,
    recommendation_type: str = "similar",
    count: int = 5,
    exclude_ids: Optional[list] = None,
) -> Dict[str, Any]:
    """Get anime recommendations"""
    cache = CacheService()
    anilist = AniListClient()

    # If title provided instead of ID, search for it
    if reference_title and not reference_anime_id:
        search_result = await anilist.search_media(
            {"search": reference_title, "page": 1, "perPage": 1, "type": "ANIME"}
        )
        media_list = search_result.get("Page", {}).get("media", [])
        if media_list:
            reference_anime_id = media_list[0].get("id")

    if not reference_anime_id:
        return {"error": "Could not find reference anime"}

    cache_key = f"recommendations:{reference_anime_id}:{recommendation_type}:{count}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    # Get recommendations from AniList
    result = await anilist.get_recommendations(reference_anime_id)

    recommendations = (
        result.get("Media", {}).get("recommendations", {}).get("nodes", [])
    )

    # Filter excluded IDs
    if exclude_ids:
        recommendations = [
            r
            for r in recommendations
            if r.get("mediaRecommendation", {}).get("id") not in exclude_ids
        ]

    # Take top N
    recommendations = recommendations[:count]

    formatted = {
        "reference_anime_id": reference_anime_id,
        "recommendation_type": recommendation_type,
        "recommendations": [
            {
                "anime": rec.get("mediaRecommendation", {}),
                "rating": rec.get("rating"),
                "user_rating": rec.get("userRating"),
            }
            for rec in recommendations
        ],
    }

    await cache.set(cache_key, formatted, ttl=3600)  # 1 hour

    return formatted


# Register tools
registry.register(
    MCPTool(
        name="get_user_list",
        description="Get a user's anime/manga list from AniList",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "AniList user ID"},
                "user_name": {"type": "string", "description": "AniList username"},
                "list_type": {
                    "type": "string",
                    "enum": ["ANIME", "MANGA"],
                    "default": "ANIME",
                },
                "status": {
                    "type": "string",
                    "enum": [
                        "CURRENT",
                        "PLANNING",
                        "COMPLETED",
                        "DROPPED",
                        "PAUSED",
                        "REPEATING",
                    ],
                },
                "sort": {
                    "type": "string",
                    "enum": [
                        "SCORE",
                        "PROGRESS",
                        "UPDATED_TIME",
                        "STARTED_ON",
                        "FINISHED_ON",
                    ],
                    "default": "UPDATED_TIME",
                },
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 50, "maximum": 500},
            },
        },
        handler=get_user_list_handler,
    )
)

registry.register(
    MCPTool(
        name="get_anime_recommendations",
        description="Get personalized anime recommendations based on reference anime",
        parameters={
            "type": "object",
            "properties": {
                "reference_anime_id": {
                    "type": "integer",
                    "description": "AniList ID of reference anime",
                },
                "reference_title": {
                    "type": "string",
                    "description": "Title of reference anime",
                },
                "recommendation_type": {
                    "type": "string",
                    "enum": ["similar", "taste_profile", "trending_genre"],
                    "default": "similar",
                },
                "count": {"type": "integer", "default": 5, "maximum": 20},
                "exclude_ids": {"type": "array", "items": {"type": "integer"}},
            },
        },
        handler=get_anime_recommendations_handler,
    )
)
