"""
Unit tests for services
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from src.services.cache.cache_service import CacheService


class TestCacheService:
    @pytest.mark.asyncio
    async def test_cache_get(self, mock_redis):
        """Test cache get operation"""
        expected_value = {"test": "data"}
        mock_redis.get = AsyncMock(return_value=expected_value)

        with patch(
            "src.services.cache.cache_service.RedisClient", return_value=mock_redis
        ):
            cache = CacheService()
            result = await cache.get("test_key")

        assert result == expected_value


class TestAniListClient:
    @pytest.mark.asyncio
    async def test_search_media(self):
        """Test AniList search media"""
        # This would require mocking the GraphQL client
        pass
