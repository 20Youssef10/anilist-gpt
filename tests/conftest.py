"""
Test fixtures and utilities
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from src.services.cache.redis_client import RedisClient
from src.services.anilist.client import AniListClient


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    redis_mock = Mock(spec=RedisClient)
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.set = AsyncMock(return_value=True)
    redis_mock.delete = AsyncMock(return_value=True)
    return redis_mock


@pytest.fixture
def mock_anilist():
    """Mock AniList client"""
    client_mock = Mock(spec=AniListClient)
    client_mock.search_media = AsyncMock(
        return_value={"Page": {"media": [], "pageInfo": {"total": 0, "currentPage": 1}}}
    )
    return client_mock


@pytest.fixture
def sample_anime_response():
    """Sample anime search response"""
    return {
        "Page": {
            "media": [
                {
                    "id": 1,
                    "title": {
                        "english": "Attack on Titan",
                        "romaji": "Shingeki no Kyojin",
                    },
                    "description": "Humans fight against giant humanoid creatures...",
                    "coverImage": {"large": "https://example.com/cover.jpg"},
                    "genres": ["Action", "Drama", "Fantasy"],
                    "episodes": 25,
                    "averageScore": 84,
                    "status": "FINISHED",
                }
            ],
            "pageInfo": {
                "total": 1,
                "currentPage": 1,
                "lastPage": 1,
                "hasNextPage": False,
            },
        }
    }
