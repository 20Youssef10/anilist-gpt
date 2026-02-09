"""
Anime search and discovery tools
"""

import hashlib
import json
from typing import Dict, Any, Optional

from src.tools.registry import registry, MCPTool
from src.services.anilist.client import AniListClient
from src.services.cache.cache_service import CacheService


async def search_anime_handler(
    query: Optional[str] = None,
    genres: Optional[list] = None,
    tags: Optional[list] = None,
    season: Optional[str] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    format: Optional[str] = None,
    minimum_score: Optional[int] = None,
    sort: str = "POPULARITY_DESC",
    page: int = 1,
    per_page: int = 10,
) -> Dict[str, Any]:
    """Search for anime with filters"""
    cache = CacheService()
    anilist = AniListClient()

    # Generate cache key
    cache_params = {
        "q": query,
        "g": genres,
        "t": tags,
        "s": season,
        "y": year,
        "st": status,
        "f": format,
        "min": minimum_score,
        "sort": sort,
        "p": page,
        "pp": per_page,
    }
    cache_key = f"search:{hashlib.md5(str(cache_params).encode()).hexdigest()}"

    # Try cache
    cached = await cache.get(cache_key)
    if cached:
        return cached

    # Build GraphQL variables
    variables = {"page": page, "perPage": per_page, "sort": sort, "type": "ANIME"}

    # Add filters
    if query:
        variables["search"] = query
    if genres:
        variables["genre_in"] = genres
    if tags:
        variables["tag_in"] = tags
    if season:
        variables["season"] = season
    if year:
        variables["seasonYear"] = year
    if status:
        variables["status"] = status
    if format:
        variables["format"] = format
    if minimum_score:
        variables["averageScore_greater"] = minimum_score

    # Execute query
    result = await anilist.search_media(variables)

    # Format for ChatGPT
    formatted = {
        "results": result.get("Page", {}).get("media", []),
        "page_info": result.get("Page", {}).get("pageInfo", {}),
        "widget_html": generate_search_widget(result.get("Page", {}).get("media", [])),
        "text_summary": format_search_summary(result.get("Page", {}).get("media", [])),
    }

    # Cache results
    await cache.set(cache_key, formatted, ttl=3600)

    return formatted


def format_search_summary(media_list: list) -> str:
    """Generate human-readable summary"""
    if not media_list:
        return "No results found matching your criteria."

    summaries = []
    for media in media_list[:5]:
        title = media.get("title", {}).get("english") or media.get("title", {}).get(
            "romaji", "Unknown"
        )
        score = media.get("averageScore", "N/A")
        episodes = media.get("episodes", "?")
        summaries.append(f"• {title} (Score: {score}/100, {episodes} eps)")

    return "\n".join(summaries)


def generate_search_widget(media_list: list) -> str:
    """Generate HTML widget for ChatGPT"""
    if not media_list:
        return "<div>No results found</div>"

    cards = []
    for media in media_list:
        title = media.get("title", {}).get("english") or media.get("title", {}).get(
            "romaji", "Unknown"
        )
        image = media.get("coverImage", {}).get("large", "")
        score = media.get("averageScore", 0)
        episodes = media.get("episodes", "?")
        genres = media.get("genres", [])[:3]

        cards.append(f"""
        <div class="anime-card" data-id="{media.get("id")}">
            <img src="{image}" alt="{title}" />
            <div class="info">
                <h4>{title}</h4>
                <div class="meta">
                    <span class="score">★ {score / 10:.1f}</span>
                    <span class="episodes">{episodes} eps</span>
                </div>
                <div class="genres">{", ".join(genres)}</div>
            </div>
        </div>
        """)

    return f"""
    <div class="anime-search-results">
        <style>
            .anime-search-results {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }}
            .anime-card {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; cursor: pointer; }}
            .anime-card img {{ width: 100%; height: 280px; object-fit: cover; }}
            .anime-card .info {{ padding: 12px; }}
            .anime-card h4 {{ margin: 0 0 8px 0; font-size: 14px; }}
            .anime-card .meta {{ display: flex; justify-content: space-between; font-size: 12px; color: #666; }}
            .anime-card .genres {{ font-size: 11px; color: #999; margin-top: 4px; }}
        </style>
        {"".join(cards)}
    </div>
    """


# Register tool
registry.register(
    MCPTool(
        name="search_anime",
        description="Search for anime by title, genre, season, or custom filters",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string (title keywords)",
                },
                "genres": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by genres",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by tags",
                },
                "season": {
                    "type": "string",
                    "enum": ["WINTER", "SPRING", "SUMMER", "FALL"],
                },
                "year": {"type": "integer", "description": "Filter by year"},
                "status": {
                    "type": "string",
                    "enum": [
                        "FINISHED",
                        "RELEASING",
                        "NOT_YET_RELEASED",
                        "CANCELLED",
                        "HIATUS",
                    ],
                },
                "format": {
                    "type": "string",
                    "enum": [
                        "TV",
                        "TV_SHORT",
                        "MOVIE",
                        "SPECIAL",
                        "OVA",
                        "ONA",
                        "MUSIC",
                    ],
                },
                "minimum_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "sort": {
                    "type": "string",
                    "enum": [
                        "POPULARITY_DESC",
                        "SCORE_DESC",
                        "TRENDING_DESC",
                        "START_DATE_DESC",
                    ],
                    "default": "POPULARITY_DESC",
                },
                "page": {"type": "integer", "default": 1, "minimum": 1},
                "per_page": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50,
                },
            },
        },
        handler=search_anime_handler,
    )
)
