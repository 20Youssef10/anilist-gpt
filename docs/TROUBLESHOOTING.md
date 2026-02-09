# Troubleshooting Guide

## 🔧 Common Issues & Solutions

### Issue 1: App Won't Start

**Symptoms:**
```
Error: Application failed to start
```

**Solutions:**

1. **Check environment variables:**
   ```bash
   fly secrets list --app anilist-gpt
   # Verify all required secrets are set
   ```

2. **Check logs:**
   ```bash
   fly logs --app anilist-gpt
   ```

3. **Verify database connection:**
   ```bash
   fly postgres connect --app anilist-gpt-db
   ```

4. **Redeploy:**
   ```bash
   fly deploy --app anilist-gpt
   ```

---

### Issue 2: Database Connection Fails

**Symptoms:**
```
Connection refused to database
```

**Solutions:**

1. **Check if database is running:**
   ```bash
   fly status --app anilist-gpt-db
   ```

2. **Verify connection string:**
   ```bash
   fly secrets list --app anilist-gpt | grep DATABASE
   ```

3. **Check database is attached:**
   ```bash
   fly postgres attach anilist-gpt-db --app anilist-gpt
   ```

4. **Test connection:**
   ```bash
   fly postgres connect --app anilist-gpt-db
   ```

---

### Issue 3: Redis Connection Timeout

**Symptoms:**
```
Redis connection timeout
Cache errors
```

**Solutions:**

1. **Check Redis status:**
   ```bash
   fly redis status anilist-gpt-redis
   ```

2. **Verify Redis URL:**
   ```bash
   fly secrets list --app anilist-gpt | grep REDIS
   ```

3. **Check network connectivity:**
   ```bash
   fly ssh console --app anilist-gpt
   # Then test: redis-cli -u $REDIS_URL ping
   ```

4. **Restart app:**
   ```bash
   fly apps restart anilist-gpt
   ```

---

### Issue 4: OAuth Login Fails

**Symptoms:**
```
OAuth error: redirect_uri_mismatch
Token exchange failed
```

**Solutions:**

1. **Verify redirect URL in AniList:**
   - Go to https://anilist.co/settings/developer
   - Check redirect URL matches exactly:
     - Production: `https://anilist-gpt.fly.dev/auth/callback`
     - Local: `http://localhost:8000/auth/callback`

2. **Check secrets:**
   ```bash
   fly secrets list --app anilist-gpt | grep ANILIST
   ```

3. **Verify AniList API status:**
   ```bash
   curl https://graphql.anilist.co \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "{Viewer{id}}"}'
   ```

---

### Issue 5: MCP Tools Not Responding

**Symptoms:**
```
Tool not found
Method not found
```

**Solutions:**

1. **Check tool registration:**
   ```python
   # In Python console
   from src.tools.registry import registry
   print([t.name for t in registry.list_tools()])
   ```

2. **Test MCP directly:**
   ```bash
   curl -X POST https://anilist-gpt.fly.dev/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/list",
       "id": 1
     }'
   ```

3. **Check for import errors in logs:**
   ```bash
   fly logs --app anilist-gpt | grep -i error
   ```

---

### Issue 6: High Memory Usage

**Symptoms:**
```
OOMKilled
High memory usage alert
```

**Solutions:**

1. **Check current usage:**
   ```bash
   fly status --app anilist-gpt
   ```

2. **Scale up memory:**
   ```bash
   fly scale memory 2048 --app anilist-gpt
   ```

3. **Check for memory leaks:**
   ```bash
   fly logs --app anilist-gpt | grep -i memory
   ```

4. **Optimize cache TTL:**
   - Reduce cache TTL in settings
   - Clear old cache entries

---

### Issue 7: Slow Response Times

**Symptoms:**
```
Request timeout
High latency
```

**Solutions:**

1. **Check database queries:**
   ```bash
   # Enable query logging
   fly logs --app anilist-gpt | grep -i "slow query"
   ```

2. **Verify caching is working:**
   ```bash
   # Check cache hit rate
   curl https://anilist-gpt.fly.dev/metrics
   ```

3. **Scale up CPU:**
   ```bash
   fly scale cpu 2 --app anilist-gpt
   ```

4. **Check AniList API rate limits:**
   - Monitor rate limit headers
   - Implement request batching

---

### Issue 8: CI/CD Build Fails

**Symptoms:**
```
Build failed in GitHub Actions
Docker build error
```

**Solutions:**

1. **Check build logs:**
   - Go to: https://github.com/20Youssef10/anilist-gpt/actions
   - Click on failed workflow
   - View logs

2. **Test build locally:**
   ```bash
   docker build -f docker/Dockerfile -t anilist-gpt:test .
   ```

3. **Check secrets are set:**
   - Verify all secrets in GitHub Settings → Secrets → Actions

4. **Update dependencies:**
   ```bash
   pip freeze > requirements/base.txt
   git add requirements/
   git commit -m "Update dependencies"
   git push
   ```

---

### Issue 9: Tests Failing

**Symptoms:**
```
pytest failed
Test suite errors
```

**Solutions:**

1. **Run tests locally:**
   ```bash
   pytest tests/unit -v
   ```

2. **Check test database:**
   ```bash
   # Ensure test DB is accessible
   psql $DATABASE_URL -c "SELECT 1"
   ```

3. **Run with coverage:**
   ```bash
   pytest --cov=src --cov-report=html
   # Open htmlcov/index.html
   ```

4. **Debug specific test:**
   ```bash
   pytest tests/unit/test_tools.py::TestSearchAnimeTool -v -s
   ```

---

### Issue 10: Deployment Stuck

**Symptoms:**
```
Deployment pending
Stuck in "pending" state
```

**Solutions:**

1. **Check deployment status:**
   ```bash
   fly status --app anilist-gpt
   ```

2. **Cancel stuck deployment:**
   ```bash
   fly deploy --app anilist-gpt --cancel
   ```

3. **Force new deployment:**
   ```bash
   fly deploy --app anilist-gpt --force
   ```

4. **Check for errors:**
   ```bash
   fly logs --app anilist-gpt | grep -i "error\|fail"
   ```

---

## 🆘 Emergency Procedures

### Rollback to Previous Version

```bash
# List releases
fly releases list --app anilist-gpt

# Rollback to specific version
fly releases rollback <version> --app anilist-gpt

# Or rollback to previous
fly releases rollback --app anilist-gpt
```

### Scale to Zero (Emergency)

```bash
# Stop all machines
fly apps restart anilist-gpt

# Or scale to zero
fly scale count 0 --app anilist-gpt
```

### Reset Database

⚠️ **WARNING: This will delete all data!**

```bash
# Create backup first
fly postgres backup create --app anilist-gpt-db

# Reset
fly postgres restart --app anilist-gpt-db
```

---

## 📞 Getting Help

### Resources

1. **Fly.io Documentation**
   - https://fly.io/docs/

2. **AniList API Docs**
   - https://anilist.gitbook.io/anilist-apiv2-docs/

3. **FastAPI Documentation**
   - https://fastapi.tiangolo.com/

4. **GitHub Issues**
   - https://github.com/20Youssef10/anilist-gpt/issues

### Debug Commands

```bash
# Full system status
fly status --all --app anilist-gpt

# Recent logs
fly logs --app anilist-gpt --recent

# SSH into app
fly ssh console --app anilist-gpt

# Check environment
fly ssh console --app anilist-gpt --command "env"

# Test network
fly ssh console --app anilist-gpt --command "curl -v https://graphql.anilist.co"
```

---

## ✅ Pre-Launch Checklist

Before going live, verify:

- [ ] All health checks passing
- [ ] Database migrations run
- [ ] Redis connection working
- [ ] OAuth flow tested
- [ ] All MCP tools responding
- [ ] Secrets configured
- [ ] Monitoring enabled
- [ ] SSL certificate valid
- [ ] Domain configured (if using custom domain)
- [ ] Rate limits configured
- [ ] Backups enabled
