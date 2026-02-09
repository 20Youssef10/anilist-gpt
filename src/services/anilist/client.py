"""
AniList GraphQL client
"""

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


class AniListClient:
    """GraphQL client for AniList API"""

    def __init__(self):
        self.endpoint = "https://graphql.anilist.co"
        self.transport = AIOHTTPTransport(url=self.endpoint)
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True,
        )
        self.rate_limit_remaining = 90
        self.rate_limit_reset = 60

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def execute(self, query: str, variables: dict = None) -> dict:
        """Execute GraphQL query with retry logic"""
        if self.rate_limit_remaining < 5:
            await asyncio.sleep(self.rate_limit_reset)

        try:
            result = await self.client.execute_async(
                gql(query), variable_values=variables
            )
            return result
        except TransportQueryError as e:
            if "429" in str(e):
                await asyncio.sleep(60)
                raise
            raise

    async def search_media(self, variables: dict) -> dict:
        """Search anime/manga with filters"""
        query = """
        query ($page: Int, $perPage: Int, $search: String, $sort: [MediaSort], 
               $type: MediaType, $genre_in: [String], $tag_in: [String],
               $season: MediaSeason, $seasonYear: Int, $status: MediaStatus,
               $format: MediaFormat, $averageScore_greater: Int) {
            Page(page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media(search: $search, sort: $sort, type: $type,
                      genre_in: $genre_in, tag_in: $tag_in,
                      season: $season, seasonYear: $seasonYear,
                      status: $status, format: $format,
                      averageScore_greater: $averageScore_greater) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description(asHtml: false)
                    coverImage {
                        large
                        medium
                    }
                    bannerImage
                    genres
                    tags {
                        name
                        rank
                    }
                    studios {
                        nodes {
                            name
                        }
                    }
                    episodes
                    duration
                    status
                    season
                    seasonYear
                    averageScore
                    popularity
                    trending
                    format
                    source
                    startDate {
                        year
                        month
                        day
                    }
                    nextAiringEpisode {
                        episode
                        timeUntilAiring
                        airingAt
                    }
                    trailer {
                        id
                        site
                    }
                }
            }
        }
        """
        return await self.execute(query, variables)

    async def get_character(self, character_id: int) -> dict:
        """Get character information"""
        query = """
        query ($id: Int!) {
            Character(id: $id) {
                id
                name {
                    full
                    native
                    alternative
                }
                image {
                    large
                    medium
                }
                description
                gender
                dateOfBirth {
                    month
                    day
                }
                age
                favourites
                media(page: 1, perPage: 10) {
                    nodes {
                        id
                        title {
                            english
                            romaji
                        }
                        type
                        coverImage {
                            large
                        }
                    }
                    edges {
                        characterRole
                        voiceActors(language: JAPANESE) {
                            id
                            name {
                                full
                            }
                            image {
                                medium
                            }
                        }
                    }
                }
            }
        }
        """
        return await self.execute(query, {"id": character_id})

    async def get_user_list(self, variables: dict) -> dict:
        """Get user anime/manga list"""
        query = """
        query ($userId: Int, $userName: String, $type: MediaType) {
            MediaListCollection(userId: $userId, userName: $userName, type: $type) {
                user {
                    id
                    name
                    avatar {
                        large
                    }
                }
                lists {
                    name
                    status
                    entries {
                        id
                        media {
                            id
                            title {
                                english
                                romaji
                            }
                            coverImage {
                                large
                            }
                            episodes
                            averageScore
                        }
                        score
                        progress
                        status
                        repeat
                        startedAt {
                            year
                            month
                            day
                        }
                        completedAt {
                            year
                            month
                            day
                        }
                    }
                }
            }
        }
        """
        return await self.execute(query, variables)

    async def get_recommendations(self, anime_id: int) -> dict:
        """Get anime recommendations"""
        query = """
        query ($id: Int!) {
            Media(id: $id) {
                id
                recommendations(page: 1, perPage: 10, sort: RATING_DESC) {
                    nodes {
                        id
                        rating
                        userRating
                        mediaRecommendation {
                            id
                            title {
                                english
                                romaji
                            }
                            coverImage {
                                large
                            }
                            averageScore
                        }
                    }
                }
            }
        }
        """
        return await self.execute(query, {"id": anime_id})

    async def get_airing_schedule(self, variables: dict) -> dict:
        """Get airing schedule"""
        query = """
        query ($page: Int, $airingAt_greater: Int, $airingAt_lesser: Int) {
            Page(page: $page, perPage: 50) {
                airingSchedules(
                    airingAt_greater: $airingAt_greater
                    airingAt_lesser: $airingAt_lesser
                ) {
                    id
                    episode
                    airingAt
                    timeUntilAiring
                    media {
                        id
                        title {
                            english
                            romaji
                        }
                        coverImage {
                            large
                        }
                        duration
                    }
                }
            }
        }
        """
        return await self.execute(query, variables)
