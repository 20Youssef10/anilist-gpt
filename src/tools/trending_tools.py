"""
Trending and seasonal anime tools
"""

from typing import Dict, Any, Optional

from src.tools.registry import registry, MCPTool
from src.services.anilist.client import AniListClient
from src.services.cache.cache_service import CacheService


async def get_trending_anime_handler(
    media_type: str = "ANIME", page: int = 1, per_page: int = 10
) -> Dict[str, Any]:
    """Get currently trending anime"""
    cache = CacheService()
    anilist = AniListClient()

    cache_key = f"trending:{media_type}:{page}:{per_page}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    variables = {
        "page": page,
        "perPage": per_page,
        "sort": "TRENDING_DESC",
        "type": media_type,
    }

    result = await anilist.search_media(variables)

    formatted = {
        "results": result.get("Page", {}).get("media", []),
        "page_info": result.get("Page", {}).get("pageInfo", {}),
        "text_summary": f"Showing {per_page} trending {media_type.lower()} titles",
    }

    await cache.set(cache_key, formatted, ttl=1800)  # 30 minutes

    return formatted


async def get_seasonal_anime_handler(
    season: Optional[str] = None,
    year: Optional[int] = None,
    page: int = 1,
    per_page: int = 25,
) -> Dict[str, Any]:
    """Get anime for a specific season"""
    cache = CacheService()
    anilist = AniListClient()

    # Default to current season if not specified
    if not season or not year:
        from datetime import datetime

        now = datetime.now()
        year = year or now.year

        if not season:
            month = now.month
            if month in [12, 1, 2]:
                season = "WINTER"
            elif month in [3, 4, 5]:
                season = "SPRING"
            elif month in [6, 7, 8]:
                season = "SUMMER"
            else:
                season = "FALL"

    cache_key = f"seasonal:{season}:{year}:{page}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    variables = {
        "page": page,
        "perPage": per_page,
        "sort": "POPULARITY_DESC",
        "type": "ANIME",
        "season": season,
        "seasonYear": year,
    }

    result = await anilist.search_media(variables)

    formatted = {
        "season": season,
        "year": year,
        "results": result.get("Page", {}).get("media", []),
        "page_info": result.get("Page", {}).get("pageInfo", {}),
    }

    await cache.set(cache_key, formatted, ttl=86400)  # 24 hours

    return formatted


# Register tools
registry.register(
    MCPTool(
        name="get_trending_anime",
        description="Get currently trending anime based on AniList activity",
        parameters={
            "type": "object",
            "properties": {
                "media_type": {
                    "type": "string",
                    "enum": ["ANIME", "MANGA"],
                    "default": "ANIME",
                },
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 10, "maximum": 50},
            },
        },
        handler=get_trending_anime_handler,
    )
)

registry.register(
    MCPTool(
        name="get_seasonal_anime",
        description="Get anime for a specific season and year",
        parameters={
            "type": "object",
            "properties": {
                "season": {
                    "type": "string",
                    "enum": ["WINTER", "SPRING", "SUMMER", "FALL"],
                },
                "year": {"type": "integer"},
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 25, "maximum": 50},
            },
        },
        handler=get_seasonal_anime_handler,
    )
)
