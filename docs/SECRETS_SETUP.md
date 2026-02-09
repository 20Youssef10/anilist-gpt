# Secrets Setup Guide

This guide explains how to obtain all the required secrets for the AniList GPT deployment.

## 🔐 Required Secrets

### 1. ANILIST_CLIENT_ID & ANILIST_CLIENT_SECRET

**Purpose**: OAuth authentication with AniList API

**How to obtain:**

1. Go to https://anilist.co/settings/developer
2. Click "Create New Client"
3. Fill in the form:
   - **Name**: AniList GPT
   - **Redirect URL**: `https://anilist-gpt.fly.dev/auth/callback` (production)
   - **Redirect URL**: `http://localhost:8000/auth/callback` (local dev)
4. Click "Save"
5. Copy the **Client ID** and **Client Secret**

**Where to add:**
- GitHub Actions: `ANILIST_CLIENT_ID` and `ANILIST_CLIENT_SECRET`
- Fly.io: Same values

---

### 2. FLY_API_TOKEN

**Purpose**: Deploy to Fly.io from GitHub Actions

**How to obtain:**

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   fly auth login
   ```

3. Create API token:
   ```bash
   fly tokens create deploy -x 999999h
   ```
   
4. Copy the token (starts with `FlyV1`...)

**Where to add:**
- GitHub Actions: `FLY_API_TOKEN`

---

### 3. SECRET_KEY

**Purpose**: JWT token signing and session encryption

**How to generate:**

```bash
# Generate a secure random key
openssl rand -base64 32
```

Or use Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Where to add:**
- Fly.io production: `fly secrets set SECRET_KEY="your-generated-key" --app anilist-gpt`
- GitHub Actions (optional): `SECRET_KEY`

---

### 4. DATABASE_URL

**Purpose**: PostgreSQL database connection

**Option A: Fly.io PostgreSQL (Recommended)**

```bash
# Create database
fly postgres create --name anilist-gpt-db --region iad

# Get connection string
fly postgres attach anilist-gpt-db --app anilist-gpt
```

The URL will be automatically set as a secret.

**Option B: External Database (Railway, Supabase, etc.)**

1. Create database on your provider
2. Get connection string:
   ```
   postgresql://username:password@host:port/database
   ```
3. Set in Fly.io:
   ```bash
   fly secrets set DATABASE_URL="your-connection-string" --app anilist-gpt
   ```

---

### 5. REDIS_URL

**Purpose**: Redis cache connection

**Option A: Fly.io Redis (Upstash)**

```bash
# Create Redis
fly redis create --name anilist-gpt-redis --region iad

# Get connection string
fly redis connect anilist-gpt-redis
```

**Option B: External Redis**

1. Create Redis instance (Redis Cloud, Upstash, etc.)
2. Get connection string:
   ```
   redis://username:password@host:port
   ```
3. Set in Fly.io:
   ```bash
   fly secrets set REDIS_URL="your-redis-url" --app anilist-gpt
   ```

---

### 6. SENTRY_DSN (Optional)

**Purpose**: Error tracking and monitoring

**How to obtain:**

1. Go to https://sentry.io
2. Create account or login
3. Create new project:
   - Platform: Python
   - Project name: anilist-gpt
4. Copy the DSN:
   ```
   https://xxx@yyy.ingest.sentry.io/zzz
   ```

**Where to add:**
- GitHub Actions: `SENTRY_DSN`
- Fly.io: `fly secrets set SENTRY_DSN="your-dsn" --app anilist-gpt`

---

## 📋 Summary of All Secrets

| Secret Name | Source | GitHub Actions | Fly.io |
|------------|--------|----------------|---------|
| `ANILIST_CLIENT_ID` | AniList Developer Settings | ✅ | ✅ |
| `ANILIST_CLIENT_SECRET` | AniList Developer Settings | ✅ | ✅ |
| `FLY_API_TOKEN` | `fly tokens create` | ✅ | ❌ |
| `SECRET_KEY` | Generated with openssl | ✅ (optional) | ✅ |
| `DATABASE_URL` | Fly Postgres or external | ❌ | ✅ (auto) |
| `REDIS_URL` | Fly Redis or external | ❌ | ✅ (auto) |
| `SENTRY_DSN` | Sentry.io | ✅ | ✅ (optional) |
| `PRODUCTION_URL` | Your Fly.io app URL | ✅ | ❌ |
| `SENTRY_AUTH_TOKEN` | Sentry Settings | ✅ | ❌ |
| `SENTRY_ORG` | Sentry Organization | ✅ | ❌ |
| `SENTRY_PROJECT` | Sentry Project | ✅ | ❌ |

---

## 🚀 Quick Setup Commands

### Step 1: Create Fly.io Apps

```bash
# Create production app
fly apps create anilist-gpt

# Create staging app (optional)
fly apps create anilist-gpt-staging
```

### Step 2: Set Secrets in Fly.io

```bash
# Set AniList credentials
fly secrets set \
  ANILIST_CLIENT_ID="your-client-id" \
  ANILIST_CLIENT_SECRET="your-client-secret" \
  --app anilist-gpt

# Set security key
fly secrets set \
  SECRET_KEY="$(openssl rand -base64 32)" \
  --app anilist-gpt

# Set environment
fly secrets set \
  ENVIRONMENT="production" \
  DEBUG="false" \
  --app anilist-gpt
```

### Step 3: Create Database and Cache

```bash
# PostgreSQL
fly postgres create --name anilist-gpt-db --region iad
fly postgres attach anilist-gpt-db --app anilist-gpt

# Redis
fly redis create --name anilist-gpt-redis --region iad
fly redis attach anilist-gpt-redis --app anilist-gpt
```

### Step 4: Add GitHub Secrets

Go to: https://github.com/20Youssef10/anilist-gpt/settings/secrets/actions

Add these secrets:
1. `ANILIST_CLIENT_ID`
2. `ANILIST_CLIENT_SECRET`
3. `FLY_API_TOKEN`
4. `SENTRY_DSN` (optional)
5. `SENTRY_AUTH_TOKEN` (optional)
6. `SENTRY_ORG` (optional)
7. `SENTRY_PROJECT` (optional)
8. `PRODUCTION_URL` = `https://anilist-gpt.fly.dev`

---

## ✅ Verification

After setting up all secrets, verify:

```bash
# Check Fly.io secrets
fly secrets list --app anilist-gpt

# Check GitHub secrets (via web UI or CLI)
gh secret list --repo 20Youssef10/anilist-gpt

# Test deployment
git push origin main
```

---

## 🆘 Troubleshooting

**Issue**: `FLY_API_TOKEN` not working
- **Solution**: Regenerate with `fly tokens create deploy -x 999999h`

**Issue**: Database connection fails
- **Solution**: Check if database is in same region as app

**Issue**: AniList OAuth fails
- **Solution**: Verify redirect URL matches exactly (including https)

**Issue**: Redis connection timeout
- **Solution**: Check if Redis is in same private network as app
