"""
Cache service with AniList-specific caching strategies
"""

from typing import Optional, Any

from src.services.cache.redis_client import RedisClient


class CacheService:
    """High-level cache service"""

    def __init__(self):
        self.redis = RedisClient()

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        try:
            await self.redis.connect()
            return await self.redis.get(key)
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
        finally:
            await self.redis.disconnect()

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set cached value"""
        try:
            await self.redis.connect()
            return await self.redis.set(key, value, ttl=ttl)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
        finally:
            await self.redis.disconnect()

    async def delete(self, key: str) -> bool:
        """Delete cached value"""
        try:
            await self.redis.connect()
            return await self.redis.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
        finally:
            await self.redis.disconnect()

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            await self.redis.connect()
            keys = await self.redis.keys(pattern)
            if keys:
                for key in keys:
                    await self.redis.delete(key)
            return len(keys)
        except Exception as e:
            print(f"Cache invalidation error: {e}")
            return 0
        finally:
            await self.redis.disconnect()
