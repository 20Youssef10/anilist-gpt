"""
Character information tools
"""

from typing import Dict, Any, Optional

from src.tools.registry import registry, MCPTool
from src.services.anilist.client import AniListClient
from src.services.cache.cache_service import CacheService


async def get_character_info_handler(
    character_id: int,
    name: Optional[str] = None,
    include_relations: bool = True,
    include_anime: bool = True,
) -> Dict[str, Any]:
    """Get detailed information about a character"""
    cache = CacheService()
    anilist = AniListClient()

    cache_key = f"character:{character_id}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    result = await anilist.get_character(character_id)

    character = result.get("Character", {})

    formatted = {
        "id": character.get("id"),
        "name": character.get("name", {}),
        "image": character.get("image", {}),
        "description": character.get("description", ""),
        "gender": character.get("gender"),
        "age": character.get("age"),
        "date_of_birth": character.get("dateOfBirth", {}),
        "favourites": character.get("favourites", 0),
    }

    if include_anime:
        formatted["appearances"] = format_appearances(character.get("media", {}))

    await cache.set(cache_key, formatted, ttl=86400 * 7)  # 7 days

    return formatted


def format_appearances(media_data: Dict) -> list:
    """Format character anime appearances"""
    appearances = []

    nodes = media_data.get("nodes", [])
    edges = media_data.get("edges", [])

    for media, edge in zip(nodes, edges):
        appearance = {
            "media_id": media.get("id"),
            "title": media.get("title", {}),
            "type": media.get("type"),
            "cover_image": media.get("coverImage", {}),
            "role": edge.get("characterRole"),
            "voice_actors": [
                {
                    "id": va.get("id"),
                    "name": va.get("name", {}),
                    "image": va.get("image", {}),
                }
                for va in edge.get("voiceActors", [])
            ],
        }
        appearances.append(appearance)

    return appearances


# Register tool
registry.register(
    MCPTool(
        name="get_character_info",
        description="Get detailed information about a character including appearances and voice actors",
        parameters={
            "type": "object",
            "properties": {
                "character_id": {
                    "type": "integer",
                    "description": "AniList character ID",
                },
                "name": {
                    "type": "string",
                    "description": "Character name (alternative to ID)",
                },
                "include_relations": {"type": "boolean", "default": True},
                "include_anime": {"type": "boolean", "default": True},
            },
            "required": ["character_id"],
        },
        handler=get_character_info_handler,
    )
)
