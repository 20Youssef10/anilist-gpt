"""
Main FastAPI application entry point
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.api.routes import health, auth, webhooks
from src.mcp.server import MCPServer
from src.services.cache.redis_client import RedisClient
from src.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await init_db()
    app.state.redis = RedisClient()
    await app.state.redis.connect()
    app.state.mcp_server = MCPServer()
    await app.state.mcp_server.start()

    yield

    # Shutdown
    await app.state.redis.disconnect()
    await app.state.mcp_server.stop()


app = FastAPI(
    title="AniList GPT MCP Server",
    description="MCP Tool Server for AniList ChatGPT App",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AniList GPT MCP Server",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
    )
