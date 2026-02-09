# ChatGPT Anime/Manga App — Production Blueprint (AniList + MCP)

## 1️⃣ Product Vision
Build a ChatGPT-native Anime/Manga app that feels like a first‑party experience inside ChatGPT:
- **Instant search** across anime, manga, characters, studios, and staff via AniList GraphQL.
- **Interactive widgets** embedded in ChatGPT (Anime Cards, Character Views, Lists, Airing widgets) powered by the ChatGPT Apps SDK UI surface.
- **Personalized experiences** with AniList OAuth (user list, watching status, favorites, stats).
- **AI recommendations** using taste modeling (genre weights, studio affinity, embeddings).
- **Live discovery**: trending, seasonal, upcoming, and character exploration.
- **App Directory ready**: proper OAuth, privacy, reliability, and CI/CD.

User workflow example (inside ChatGPT):
1. User: “Find chill fantasy anime like Frieren.”
2. Assistant calls MCP tool `search_anime` with filters.
3. UI renders anime cards with synopsis, rating, genres, cover art, and “Add to List”.
4. User clicks “Add to List” → assistant calls `get_user_list` / `update_user_list` (future add) using OAuth.
5. Assistant proposes recommendations with “Why these?” explanations and visual widgets.

---

## 2️⃣ System Architecture

```
┌───────────────────────────┐
│        ChatGPT App         │
│  - App UI Widgets          │
│  - Orchestration           │
│  - Tool Selection          │
└─────────────┬─────────────┘
              │ MCP Tools
┌─────────────▼─────────────┐
│     MCP Tool Server       │
│  (Node.js/TS or FastAPI)  │
│  - Tool schema registry   │
│  - Auth handling          │
│  - Rate limits            │
│  - Request validation     │
└───────┬───────────┬────────┘
        │           │
        │           │
┌───────▼───────┐ ┌─▼────────────────┐
│ AniList GQL  │ │ AI Recommendation │
│ Integration  │ │ Layer             │
│ - GraphQL    │ │ - Taste vectors   │
│ - Query lib  │ │ - Embeddings      │
└───────┬───────┘ └───────┬───────────┘
        │                 │
        │           ┌─────▼──────┐
        │           │ Cache (Redis)
        │           │ - Query caches
        │           │ - User models
        │           └────────────┘
        │
┌───────▼────────┐
│ Auth Layer     │
│ - AniList OAuth│
│ - Token vault  │
└────────────────┘
```

### Data Flow
1. **ChatGPT App** requests a tool call (search, trending, user list, etc.).
2. **MCP Tool Server** validates input, checks cache, and performs AniList GraphQL request.
3. **Redis cache** serves hot results and stores normalized AniList responses + model features.
4. **AI Recommendation layer** reads user profile vectors + embeddings, merges with AniList results.
5. **App UI** renders cards and lists with action hooks.

---

## 3️⃣ Database & Data Modeling (Optional / Recommended)

If persistence is needed beyond AniList:

### Storage Options
- **Redis**: high‑speed cache + ephemeral user session/taste vectors.
- **PostgreSQL** (optional): persistent user preferences & embedding indexes.

### Example Data Models

**UserPreferences**
```json
{
  "userId": "anilist:12345",
  "favoriteGenres": ["Fantasy", "Slice of Life"],
  "studioAffinity": {"Madhouse": 0.8, "Wit Studio": 0.6},
  "tasteVector": [0.12, -0.54, ...],
  "lastUpdated": "2025-02-01T10:00:00Z"
}
```

**CachedAniListResponse**
```json
{
  "key": "search:frieren:anime",
  "payload": {"...": "AniList response"},
  "ttl": 3600
}
```

---

## 4️⃣ MCP Tool Design

### Tool Schema (JSON Examples)

**search_anime**
```json
{
  "name": "search_anime",
  "description": "Search anime by title, genre, season, or filters.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "genres": {"type": "array", "items": {"type": "string"}},
      "season": {"type": "string", "enum": ["WINTER","SPRING","SUMMER","FALL"]},
      "year": {"type": "integer"},
      "page": {"type": "integer", "default": 1},
      "perPage": {"type": "integer", "default": 10}
    },
    "required": ["query"]
  }
}
```

**get_trending_anime**
```json
{
  "name": "get_trending_anime",
  "description": "Return current trending anime.",
  "input_schema": {
    "type": "object",
    "properties": {
      "page": {"type": "integer", "default": 1},
      "perPage": {"type": "integer", "default": 10}
    }
  }
}
```

**get_season_anime**
```json
{
  "name": "get_season_anime",
  "description": "Seasonal anime list.",
  "input_schema": {
    "type": "object",
    "properties": {
      "season": {"type": "string", "enum": ["WINTER","SPRING","SUMMER","FALL"]},
      "year": {"type": "integer"},
      "page": {"type": "integer", "default": 1},
      "perPage": {"type": "integer", "default": 20}
    },
    "required": ["season", "year"]
  }
}
```

**get_user_list**
```json
{
  "name": "get_user_list",
  "description": "Fetch user anime list from AniList using OAuth.",
  "input_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["CURRENT","COMPLETED","DROPPED","PAUSED","PLANNING"]},
      "page": {"type": "integer", "default": 1},
      "perPage": {"type": "integer", "default": 50}
    }
  }
}
```

**get_character_info**
```json
{
  "name": "get_character_info",
  "description": "Retrieve character details and media appearances.",
  "input_schema": {
    "type": "object",
    "properties": {
      "characterId": {"type": "integer"},
      "name": {"type": "string"}
    }
  }
}
```

---

## 5️⃣ AniList GraphQL Integration

### Anime Search
```graphql
query SearchAnime($query: String, $page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(search: $query, type: ANIME) {
      id
      title { romaji english native }
      coverImage { large color }
      genres
      averageScore
      popularity
      description
      episodes
      season
      seasonYear
    }
  }
}
```

### Trending Anime
```graphql
query TrendingAnime($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: TRENDING_DESC) {
      id
      title { romaji english }
      coverImage { large }
      averageScore
      trending
    }
  }
}
```

### Seasonal Anime
```graphql
query SeasonalAnime($season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, season: $season, seasonYear: $seasonYear, sort: POPULARITY_DESC) {
      id
      title { romaji english }
      coverImage { large }
      averageScore
      popularity
      status
    }
  }
}
```

### User Lists
```graphql
query UserList($userId: Int, $status: MediaListStatus, $page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    mediaList(userId: $userId, type: ANIME, status: $status) {
      media {
        id
        title { romaji english }
        coverImage { large }
      }
      progress
      score
      status
    }
  }
}
```

### Character Data
```graphql
query CharacterInfo($id: Int, $search: String) {
  Character(id: $id, search: $search) {
    id
    name { full native }
    image { large }
    favourites
    description
    media(sort: POPULARITY_DESC) {
      nodes {
        id
        title { romaji english }
        coverImage { large }
      }
    }
  }
}
```

---

## 6️⃣ Backend Project Structure (Node.js + TypeScript)

```
/ apps
  /mcp-server
    /src
      /config
        env.ts
      /clients
        anilistClient.ts
        redisClient.ts
      /tools
        searchAnime.ts
        getTrending.ts
        getSeason.ts
        getUserList.ts
        getCharacter.ts
      /services
        anilistService.ts
        cacheService.ts
        recommendationService.ts
        authService.ts
      /routes
        oauth.ts
      /schemas
        toolSchemas.ts
      /ui
        widgets
      index.ts
    package.json
    tsconfig.json
  /ui
    /src
      /components
        AnimeCard.tsx
        CharacterView.tsx
        MediaList.tsx
      index.tsx
    package.json
    vite.config.ts
/ infra
  docker-compose.yml
  Dockerfile
  /k8s
/ .github
  /workflows
    ci.yml
```

---

## 7️⃣ Security & Privacy Design

- **OAuth token handling**: store encrypted tokens (KMS or DB encryption), use short TTL sessions.
- **Rate limiting**: Redis-based (token bucket per user/IP).
- **Input validation**: zod/jsonschema for tool inputs.
- **Secrets management**: environment variables + secret manager in production.
- **GDPR-style**: allow deletion of user preferences + cached data.

---

## 8️⃣ Testing Strategy

- **Unit Testing**: tool handlers, cache logic, query builders.
- **Integration Testing**: mock AniList API with recorded fixtures.
- **MCP Tool Testing**: validate schema, simulate ChatGPT tool calls.
- **Load Testing**: k6/Artillery for AniList rate stress.

---

## 9️⃣ CI/CD Pipeline Design

Stages:
1. **Lint & Typecheck** (eslint, tsc)
2. **Unit Tests** (jest)
3. **Integration Tests** (mocked GraphQL)
4. **Build Containers** (Docker build)
5. **Deploy** (Fly.io/Railway/Render)
6. **Smoke Tests**

Example GitHub Actions workflow:
```yaml
name: ci
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm run test
      - run: npm run build
```

---

## 🔟 Deployment Architecture

- **Dockerized MCP server** with environment variables for AniList API + OAuth.
- **UI hosting** via Vercel (static bundle from /apps/ui).
- **Compute hosting** via Fly.io or Railway with autoscaling.
- **Redis** from managed provider (Upstash, Redis Cloud).
- **Observability**: structured logs (pino), error monitoring (Sentry), metrics (Prometheus + Grafana).

---

# Advanced Features

## ⭐ AI Recommendation Engine
- **Taste vector modeling**: compute embeddings from watched titles + genres.
- **Genre weighting**: weight user genre affinities from list frequency & scores.
- **Studio affinity**: compute preference scores for studios.
- **Embedding similarity**: store embeddings in vector DB (pgvector) for kNN search.

## ⭐ Smart Anime Discovery
- **Trending prediction**: time‑series on AniList popularity + social signals.
- **Seasonal ranking AI**: combine AniList popularity + freshness + review scores.

## ⭐ Character Intelligence Explorer
- **Relationship mapping**: parse staff/character relations from AniList.
- **Popularity analytics**: track favourites over time (store daily snapshots).

## ⭐ Airing Notification Engine
- **Airing alerts**: schedule jobs for next episodes per tracked anime.
- **Push reminders**: use ChatGPT notifications + webhook triggers.

---

# Production Readiness Checklist
- **Scalable**: stateless MCP server + autoscaling.
- **Fault tolerant**: retries, circuit breaker for AniList API.
- **Cache optimized**: cache search + trending + seasonal results.
- **Rate limit safe**: global + per user throttling.
- **Resilient**: fallback to cached data if AniList API fails.
