# AniList GPT - Quick Start Guide

🚀 **Get your app running in 15 minutes!**

## Step 1: Get Your Secrets (5 minutes)

### 1.1 AniList OAuth Credentials
1. Go to https://anilist.co/settings/developer
2. Create new client
3. Set redirect URL: `https://anilist-gpt.fly.dev/auth/callback`
4. Copy Client ID and Client Secret

### 1.2 Fly.io API Token
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Create token
fly tokens create deploy -x 999999h
# Copy the token (starts with FlyV1...)
```

### 1.3 Generate Secret Key
```bash
openssl rand -base64 32
```

---

## Step 2: Add GitHub Secrets (2 minutes)

Go to: https://github.com/20Youssef10/anilist-gpt/settings/secrets/actions

Click "New repository secret" and add:

| Secret Name | Value |
|------------|-------|
| `ANILIST_CLIENT_ID` | From AniList developer settings |
| `ANILIST_CLIENT_SECRET` | From AniList developer settings |
| `FLY_API_TOKEN` | From `fly tokens create` |
| `SECRET_KEY` | Generated with openssl |
| `PRODUCTION_URL` | `https://anilist-gpt.fly.dev` |

---

## Step 3: Create Fly.io Apps (3 minutes)

```bash
# Create production app
fly apps create anilist-gpt

# Create database (auto-attaches)
fly postgres create --name anilist-gpt-db --region iad
fly postgres attach anilist-gpt-db --app anilist-gpt

# Create Redis (auto-attaches)
fly redis create --name anilist-gpt-redis --region iad
fly redis attach anilist-gpt-redis --app anilist-gpt
```

---

## Step 4: Deploy (5 minutes)

### Option A: Auto-deploy via GitHub Actions
```bash
# Push to main branch
git add .
git commit -m "Ready for deployment"
git push origin main

# Watch the magic happen at:
# https://github.com/20Youssef10/anilist-gpt/actions
```

### Option B: Manual Deploy
```bash
# Set secrets
fly secrets set \
  ANILIST_CLIENT_ID="your-id" \
  ANILIST_CLIENT_SECRET="your-secret" \
  SECRET_KEY="your-key" \
  --app anilist-gpt

# Deploy
fly deploy --app anilist-gpt
```

---

## Step 5: Verify Deployment (2 minutes)

```bash
# Test endpoints
curl https://anilist-gpt.fly.dev/health
curl https://anilist-gpt.fly.dev/health/db
curl https://anilist-gpt.fly.dev/health/redis

# Or use the test script
./scripts/test.sh
```

**Expected output:**
```json
{"status": "healthy", "service": "anilist-gpt-mcp", "version": "1.0.0"}
```

---

## Step 6: Test in ChatGPT (5 minutes)

1. Go to https://chat.openai.com
2. Click "Plugins" → "Plugin Store"
3. Click "Develop your own plugin"
4. Enter: `https://anilist-gpt.fly.dev`
5. Follow prompts to authenticate

---

## ✅ You're Done!

Your AniList GPT app is now:
- ✅ Deployed on Fly.io
- ✅ Integrated with AniList API
- ✅ Connected to ChatGPT
- ✅ Ready for users!

---

## 🆘 Troubleshooting

**Build fails?**
- Check GitHub Actions logs
- Verify all secrets are set

**App won't start?**
```bash
fly logs --app anilist-gpt
```

**Database connection fails?**
```bash
fly postgres attach anilist-gpt-db --app anilist-gpt
```

**OAuth not working?**
- Verify redirect URL in AniList settings matches exactly

---

## 📚 Next Steps

1. **Submit to ChatGPT App Directory**
   - Follow `docs/CHATGPT_SUBMISSION.md`

2. **Set up Monitoring**
   - Follow `docs/MONITORING.md`

3. **Add Custom Domain** (Optional)
   ```bash
   fly certs create yourdomain.com --app anilist-gpt
   ```

4. **Scale Up** (When needed)
   ```bash
   fly scale count 2 --app anilist-gpt
   fly scale memory 2048 --app anilist-gpt
   ```

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: https://github.com/20Youssef10/anilist-gpt/issues
- **Fly.io Docs**: https://fly.io/docs/
- **AniList API**: https://anilist.gitbook.io/

---

## 🎯 Success Checklist

- [ ] AniList OAuth credentials obtained
- [ ] GitHub secrets configured
- [ ] Fly.io app created
- [ ] Database attached
- [ ] Redis attached
- [ ] App deployed successfully
- [ ] Health checks passing
- [ ] Tested in ChatGPT
- [ ] Ready for production!

**🎉 Congratulations! Your AniList GPT is live!**
