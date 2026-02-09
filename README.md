# AniList GPT MCP Server

A production-ready ChatGPT-native application for anime and manga discovery, powered by the AniList GraphQL API.

## Features

- **Anime Search**: Search by title, genre, season, year, and more
- **Trending & Seasonal**: Discover what's popular and airing now
- **Character Info**: Deep character profiles and appearances
- **User Lists**: Access personal anime/manga lists (OAuth required)
- **AI Recommendations**: Smart anime suggestions based on your taste

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- AniList API credentials

### Installation

1. Clone the repository:
```bash
git clone https://github.com/20Youssef10/anilist-gpt.git
cd anilist-gpt
```

2. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
python -m src.main
```

The server will be available at `http://localhost:8000`

### Docker Setup

```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Application secret key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `ANILIST_CLIENT_ID` | AniList OAuth client ID | Yes |
| `ANILIST_CLIENT_SECRET` | AniList OAuth client secret | Yes |
| `ANILIST_REDIRECT_URI` | OAuth redirect URI | Yes |

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /health/db` - Database health check
- `GET /health/redis` - Redis health check
- `GET /auth/login` - AniList OAuth login
- `GET /auth/callback` - OAuth callback
- `POST /mcp` - MCP protocol endpoint

## MCP Tools

The following tools are available for ChatGPT integration:

- `search_anime` - Search anime with filters
- `get_trending_anime` - Get trending anime
- `get_seasonal_anime` - Get seasonal anime
- `get_character_info` - Get character details
- `get_user_list` - Get user anime/manga list
- `get_anime_recommendations` - Get anime recommendations

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# With coverage
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Linting
ruff check src/

# Formatting
black src/
isort src/

# Type checking
mypy src/
```

## Deployment

### Fly.io

```bash
fly deploy
```

### Environment-specific configs

- `fly.staging.toml` - Staging environment
- `fly.production.toml` - Production environment

## Architecture

```
┌─────────────────────────────────────┐
│         ChatGPT Client              │
└─────────────┬───────────────────────┘
              │ MCP Protocol
┌─────────────▼───────────────────────┐
│      FastAPI MCP Server             │
│  ┌─────────┐ ┌─────────┐           │
│  │  Tools  │ │  Auth   │           │
│  └─────────┘ └─────────┘           │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌─────────┐
│AniList│ │ Redis │ │PostgreSQL│
└───────┘ └───────┘ └─────────┘
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## Support

For issues and feature requests, please use the GitHub issue tracker.
