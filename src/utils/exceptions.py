"""
Exception classes
"""


class AniListGPTError(Exception):
    """Base application error"""

    pass


class AniListAPIError(AniListGPTError):
    """AniList API error"""

    pass


class CacheError(AniListGPTError):
    """Cache operation error"""

    pass


class AuthenticationError(AniListGPTError):
    """Authentication error"""

    pass


class RateLimitError(AniListGPTError):
    """Rate limit exceeded"""

    pass


class ValidationError(AniListGPTError):
    """Input validation error"""

    pass
