"""
Health check routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.database import get_db
from src.services.cache.redis_client import RedisClient

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": "anilist-gpt-mcp", "version": "1.0.0"}


@router.get("/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    """Database health check"""
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


@router.get("/redis")
async def health_redis():
    """Redis health check"""
    try:
        redis = RedisClient()
        await redis.connect()
        await redis.set("health_check", "ok", ttl=10)
        value = await redis.get("health_check")
        await redis.disconnect()

        if value == "ok":
            return {"status": "healthy", "redis": "connected"}
        else:
            return {"status": "unhealthy", "redis": "unexpected response"}
    except Exception as e:
        return {"status": "unhealthy", "redis": str(e)}


@router.get("/ready")
async def readiness_check():
    """Readiness probe for Kubernetes"""
    return {"ready": True}
