"""
Integration tests for AniList API
"""

import pytest
import respx
from httpx import Response

from src.services.anilist.client import AniListClient


class TestAniListAPIIntegration:
    @pytest.fixture
    def anilist_client(self):
        return AniListClient()

    @pytest.mark.asyncio
    @respx.mock
    async def test_search_media_success(self, anilist_client):
        """Test successful AniList API search"""
        route = respx.post("https://graphql.anilist.co").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "Page": {
                            "media": [{"id": 1, "title": {"romaji": "Test"}}],
                            "pageInfo": {"total": 1},
                        }
                    }
                },
            )
        )

        result = await anilist_client.search_media(
            {"search": "test", "page": 1, "perPage": 10}
        )

        assert "Page" in result
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_rate_limit_handling(self, anilist_client):
        """Test rate limit error handling"""
        respx.post("https://graphql.anilist.co").mock(
            return_value=Response(429, text="Rate limit exceeded")
        )

        with pytest.raises(Exception):
            await anilist_client.search_media({"search": "test"})
