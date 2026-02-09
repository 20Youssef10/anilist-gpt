"""
Database models and connection
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime

from src.config.settings import settings

Base = declarative_base()


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    anilist_user_id = Column(Integer, unique=True, nullable=True)
    anilist_username = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    interactions = relationship("UserAnimeInteraction", back_populates="user")


class UserAnimeInteraction(Base):
    """User anime interaction model"""

    __tablename__ = "user_anime_interactions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    anilist_anime_id = Column(Integer, nullable=False)
    status = Column(String(20))  # watching, completed, dropped, etc.
    score = Column(Integer)
    progress = Column(Integer, default=0)
    favorite = Column(Boolean, default=False)
    interacted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="interactions")


class CachedAnime(Base):
    """Cached anime data"""

    __tablename__ = "cached_anime"

    anilist_id = Column(Integer, primary_key=True)
    title_english = Column(String(500))
    title_romaji = Column(String(500))
    description = Column(Text)
    genres = Column(Text)  # JSON string
    tags = Column(Text)  # JSON string
    studios = Column(Text)  # JSON string
    episodes = Column(Integer)
    duration = Column(Integer)
    status = Column(String(50))
    season = Column(String(20))
    season_year = Column(Integer)
    average_score = Column(Integer)
    popularity = Column(Integer)
    cover_image_url = Column(Text)
    banner_image_url = Column(Text)
    cached_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


# Database engine and session
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Get database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
