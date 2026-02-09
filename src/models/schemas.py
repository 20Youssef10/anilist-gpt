"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AnimeSearchParams(BaseModel):
    """Anime search parameters"""

    query: Optional[str] = Field(None, max_length=200)
    genres: Optional[List[str]] = Field(None, max_length=10)
    tags: Optional[List[str]] = Field(None, max_length=10)
    season: Optional[str] = Field(None, regex="^(WINTER|SPRING|SUMMER|FALL)$")
    year: Optional[int] = Field(None, ge=1940, le=2030)
    status: Optional[str] = None
    format: Optional[str] = None
    minimum_score: Optional[int] = Field(None, ge=0, le=100)
    sort: str = "POPULARITY_DESC"
    page: int = Field(1, ge=1, le=100)
    per_page: int = Field(10, ge=1, le=50)


class CharacterQuery(BaseModel):
    """Character query parameters"""

    character_id: Optional[int] = Field(None, ge=1)
    name: Optional[str] = Field(None, max_length=100)
    include_relations: bool = True
    include_anime: bool = True


class UserListParams(BaseModel):
    """User list parameters"""

    user_id: Optional[int] = None
    user_name: Optional[str] = None
    list_type: str = "ANIME"
    status: Optional[str] = None
    sort: str = "UPDATED_TIME"
    page: int = 1
    per_page: int = Field(50, le=500)


class UserResponse(BaseModel):
    """User response model"""

    id: str
    anilist_user_id: Optional[int]
    anilist_username: Optional[str]
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    service: str
    version: str
