"""
Redis cache client
"""

import json
import redis.asyncio as redis
from typing import Optional, Any, List

from src.config.settings import settings


class RedisClient:
    """Async Redis client wrapper"""

    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis"""
        if not self.client:
            self.client = redis.from_url(self.redis_url, decode_responses=True)

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            self.client = None

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            await self.connect()

        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        if not self.client:
            await self.connect()

        serialized = json.dumps(value) if not isinstance(value, str) else value
        return await self.client.setex(key, ttl, serialized)

    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.client:
            await self.connect()

        result = await self.client.delete(key)
        return result > 0

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            await self.connect()

        return await self.client.exists(key) > 0

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key"""
        if not self.client:
            await self.connect()

        return await self.client.expire(key, seconds)

    async def incr(self, key: str) -> int:
        """Increment counter"""
        if not self.client:
            await self.connect()

        return await self.client.incr(key)

    async def sadd(self, key: str, *members) -> int:
        """Add members to set"""
        if not self.client:
            await self.connect()

        return await self.client.sadd(key, *members)

    async def srem(self, key: str, *members) -> int:
        """Remove members from set"""
        if not self.client:
            await self.connect()

        return await self.client.srem(key, *members)

    async def smembers(self, key: str) -> List[str]:
        """Get all members of set"""
        if not self.client:
            await self.connect()

        return list(await self.client.smembers(key))

    async def zadd(self, key: str, mapping: dict) -> int:
        """Add to sorted set"""
        if not self.client:
            await self.connect()

        return await self.client.zadd(key, mapping)

    async def zrangebyscore(
        self, key: str, min_score: float, max_score: float
    ) -> List[str]:
        """Get range from sorted set by score"""
        if not self.client:
            await self.connect()

        return await self.client.zrangebyscore(key, min_score, max_score)

    async def zrem(self, key: str, *members) -> int:
        """Remove from sorted set"""
        if not self.client:
            await self.connect()

        return await self.client.zrem(key, *members)

    async def lpush(self, key: str, *values) -> int:
        """Push to list"""
        if not self.client:
            await self.connect()

        return await self.client.lpush(key, *values)

    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern"""
        if not self.client:
            await self.connect()

        return list(await self.client.keys(pattern))

    async def mget(self, keys: List[str]) -> List[Optional[str]]:
        """Get multiple keys"""
        if not self.client:
            await self.connect()

        values = await self.client.mget(keys)
        return [v if v else None for v in values]
