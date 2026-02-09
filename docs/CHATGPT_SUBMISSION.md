# ChatGPT App Directory Submission Guide

## 📋 Prerequisites

Before submitting, ensure:
- [ ] App is deployed and running
- [ ] All MCP tools are working
- [ ] OAuth is configured (optional but recommended)
- [ ] Privacy policy is published
- [ ] Logo/icon is ready (512x512 PNG)

---

## 🚀 Step-by-Step Submission

### Step 1: Prepare Your Assets

**Logo Requirements:**
- Size: 512x512 pixels
- Format: PNG with transparency
- Style: Simple, recognizable
- Background: Transparent

**Create a simple logo:**
```bash
# Create a placeholder logo (replace with your own)
convert -size 512x512 xc:none -pointsize 30 -fill black -gravity center -annotate +0+0 "AniList GPT" logo.png
```

**Upload logo to your server:**
```bash
# Upload to your app
fly deploy --app anilist-gpt
# Place logo at /static/logo.png
```

### Step 2: Get OpenAI Verification Token

1. Go to https://platform.openai.com/apps
2. Click "Create App"
3. Fill in basic information
4. Copy the verification token
5. Add it to `ai-plugin.json`:
   ```json
   "verification_tokens": {
     "openai": "YOUR_VERIFICATION_TOKEN"
   }
   ```

### Step 3: Update ai-plugin.json

Edit `ai-plugin.json` with your:
- `verification_tokens.openai`
- `logo_url` (must be HTTPS)
- `contact_email`
- `legal_info_url`

### Step 4: Host the Manifest Files

Ensure these files are accessible:
- `/.well-known/ai-plugin.json` → Your `ai-plugin.json`
- `/openapi.json` or `/openapi.yaml` → Your OpenAPI spec
- `/logo.png` → Your app logo

**Add to your FastAPI app:**
```python
from fastapi.staticfiles import StaticFiles

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve ai-plugin.json
@app.get("/.well-known/ai-plugin.json")
async def ai_plugin():
    return FileResponse("ai-plugin.json")

# Serve OpenAPI spec
@app.get("/openapi.json")
async def openapi_spec():
    return FileResponse("openapi.json")
```

### Step 5: Test Your App

**Test the manifest:**
```bash
curl https://anilist-gpt.fly.dev/.well-known/ai-plugin.json
```

**Test the OpenAPI spec:**
```bash
curl https://anilist-gpt.fly.dev/openapi.json
```

**Test with ChatGPT:**
1. Go to ChatGPT
2. Click "Plugins" in the model selector
3. Click "Plugin Store"
4. Click "Develop your own plugin"
5. Enter: `https://anilist-gpt.fly.dev`
6. Follow the prompts

### Step 6: Submit to App Directory

1. Go to https://platform.openai.com/apps
2. Find your app
3. Click "Submit for Review"
4. Fill out the submission form:
   - **App Name**: AniList GPT
   - **Category**: Entertainment / Lifestyle
   - **Description**: AI-powered anime and manga discovery
   - **Use Cases**: 
     - Search for anime by title, genre, or season
     - Get personalized recommendations
     - Discover trending and seasonal anime
     - Explore character information
   - **Target Audience**: Anime fans, manga readers
   - **Privacy Policy**: https://anilist-gpt.fly.dev/privacy
   - **Terms of Service**: https://anilist-gpt.fly.dev/terms

5. Upload screenshots (3-5 recommended):
   - Search results
   - Recommendation interface
   - Character details
   - Trending anime

6. Submit for review

---

## 📝 Required Pages

### Privacy Policy

Create `static/privacy.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy - AniList GPT</title>
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Last updated: February 2024</p>
    
    <h2>Information We Collect</h2>
    <p>We collect information you provide through AniList OAuth, including:</p>
    <ul>
        <li>AniList user ID and username</li>
        <li>Anime/manga list data (if authorized)</li>
    </ul>
    
    <h2>How We Use Information</h2>
    <p>We use your information to:</p>
    <ul>
        <li>Provide personalized anime recommendations</li>
        <li>Access your AniList lists (with permission)</li>
        <li>Improve our recommendation algorithms</li>
    </ul>
    
    <h2>Data Storage</h2>
    <p>Your data is stored securely and encrypted. We use:</p>
    <ul>
        <li>PostgreSQL for persistent storage</li>
        <li>Redis for caching</li>
        <li>Industry-standard encryption</li>
    </ul>
    
    <h2>Your Rights</h2>
    <p>You can request deletion of your data at any time by contacting us.</p>
    
    <h2>Contact</h2>
    <p>Email: support@anilist-gpt.com</p>
</body>
</html>
```

### Terms of Service

Create `static/terms.html` with similar structure covering:
- Acceptable use
- Limitation of liability
- Service availability
- Changes to terms

---

## 🧪 Testing Checklist

Before submitting, verify:

- [ ] App responds within 5 seconds
- [ ] All tools work correctly
- [ ] OAuth flow completes successfully
- [ ] Error handling is graceful
- [ ] Rate limits are respected
- [ ] HTTPS is enforced
- [ ] CORS is configured properly
- [ ] Logo loads correctly
- [ ] Privacy policy is accessible
- [ ] Terms of service is accessible

---

## ⏱️ Timeline

- **Submission Review**: 1-2 weeks
- **Approval/Denial**: Email notification
- **Updates**: Can submit updates anytime

---

## 🎯 Tips for Approval

1. **Clear Value Proposition**: Explain why users need this
2. **Unique Features**: Highlight AI recommendations
3. **Good Error Messages**: Handle failures gracefully
4. **Fast Response**: Optimize for <3s response time
5. **Comprehensive**: Cover common use cases
6. **Well-Tested**: Ensure tools work reliably

---

## 🆘 Troubleshooting

**Issue**: Manifest not loading
- Check HTTPS is working
- Verify CORS headers
- Test with `curl -I`

**Issue**: OAuth fails
- Verify redirect URLs match exactly
- Check client ID/secret
- Test OAuth flow manually

**Issue**: Tools not working
- Check MCP server logs
- Verify tool schemas are valid
- Test tools via API directly

**Issue**: Slow responses
- Enable caching
- Optimize database queries
- Use Redis for session storage

---

## 📚 Additional Resources

- [OpenAI Plugin Documentation](https://platform.openai.com/docs/plugins/introduction)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [AniList API Docs](https://anilist.gitbook.io/anilist-apiv2-docs)
