"""
Unit tests for tools
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from src.tools.anime_tools import search_anime_handler
from src.utils.validators import SearchParams


class TestSearchAnimeTool:
    @pytest.mark.asyncio
    async def test_search_with_cache_hit(self, mock_redis):
        """Test search returns cached results"""
        cached_result = {"results": [{"id": 1, "title": "Test"}]}
        mock_redis.get = AsyncMock(return_value=cached_result)

        with patch("src.tools.anime_tools.CacheService", return_value=mock_redis):
            result = await search_anime_handler(query="test")

        assert result == cached_result
        mock_redis.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_cache_miss(self, mock_redis, sample_anime_response):
        """Test search fetches from API when cache misses"""
        mock_redis.get = AsyncMock(return_value=None)

        mock_anilist = Mock()
        mock_anilist.search_media = AsyncMock(return_value=sample_anime_response)

        with (
            patch("src.tools.anime_tools.CacheService", return_value=mock_redis),
            patch("src.tools.anime_tools.AniListClient", return_value=mock_anilist),
        ):
            result = await search_anime_handler(query="Attack on Titan")

        assert "results" in result
        assert len(result["results"]) == 1


class TestValidators:
    def test_valid_search_params(self):
        """Test valid search parameters"""
        params = SearchParams(
            query="Attack on Titan",
            genres=["Action", "Drama"],
            year=2023,
            page=1,
            per_page=10,
        )
        assert params.query == "Attack on Titan"
        assert params.year == 2023

    def test_invalid_year(self):
        """Test year validation"""
        with pytest.raises(ValueError):
            SearchParams(year=1800)
