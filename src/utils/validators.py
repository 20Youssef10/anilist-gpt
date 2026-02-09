"""
Input validators
"""

import re
from typing import Optional, List
from pydantic import BaseModel, validator


class SearchParams(BaseModel):
    """Anime search parameters validation"""

    query: Optional[str] = None
    genres: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    season: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None
    format: Optional[str] = None
    minimum_score: Optional[int] = None
    sort: str = "POPULARITY_DESC"
    page: int = 1
    per_page: int = 10

    @validator("query")
    def validate_query(cls, v):
        if v:
            if len(v) > 200:
                raise ValueError("Query too long")
            if re.search(r'[<>"\']', v):
                raise ValueError("Invalid characters in query")
        return v

    @validator("year")
    def validate_year(cls, v):
        if v and (v < 1940 or v > 2030):
            raise ValueError("Year must be between 1940 and 2030")
        return v


class CharacterQuery(BaseModel):
    """Character query validation"""

    character_id: Optional[int] = None
    name: Optional[str] = None

    @validator("name")
    def validate_name(cls, v):
        if v and len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v
