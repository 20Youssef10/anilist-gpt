# Monitoring & Observability Guide

## 📊 Overview

This guide covers setting up monitoring, logging, and alerting for the AniList GPT application.

## 🎯 Key Metrics to Monitor

### Application Metrics
- Response time (p50, p95, p99)
- Error rate
- Request throughput
- Cache hit rate
- Database connection pool

### Infrastructure Metrics
- CPU usage
- Memory usage
- Disk space
- Network latency

### Business Metrics
- Active users
- Search queries
- Recommendation accuracy
- OAuth success rate

---

## 🛠️ Setup Options

### Option 1: Fly.io Dashboard (Built-in)

Fly.io provides built-in monitoring:

```bash
# View app metrics
fly status --app anilist-gpt

# View logs
fly logs --app anilist-gpt

# View metrics dashboard
fly dashboard --app anilist-gpt
```

### Option 2: Prometheus + Grafana

**1. Add Prometheus client to app:**

```python
# Already included in requirements
# prometheus-client>=0.19.0
```

**2. Expose metrics endpoint:**

```python
from prometheus_client import make_asgi_app

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

**3. Deploy Prometheus to Fly.io:**

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'anilist-gpt'
    static_configs:
      - targets: ['anilist-gpt.fly.dev:8080']
```

**4. Deploy Grafana:**

```bash
fly apps create anilist-gpt-grafana
# Deploy Grafana container
```

### Option 3: Sentry (Error Tracking)

**Already configured in the app!**

Just add the DSN to secrets:
```bash
fly secrets set SENTRY_DSN="your-sentry-dsn" --app anilist-gpt
```

View errors at: https://sentry.io

---

## 📈 Setting Up Health Checks

### Fly.io Health Checks

Update `fly.production.toml`:

```toml
[[services.http_checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "get"
  path = "/health"
  protocol = "http"
  tls_skip_verify = false
  [services.http_checks.headers]
```

### Custom Health Checks

**Script for external monitoring (UptimeRobot, Pingdom):**

```bash
#!/bin/bash
# health-check.sh

URL="https://anilist-gpt.fly.dev/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $STATUS -eq 200 ]; then
    echo "Healthy"
    exit 0
else
    echo "Unhealthy (HTTP $STATUS)"
    exit 1
fi
```

---

## 🚨 Alerting

### Fly.io Alerts

Set up in Fly.io dashboard:
- High memory usage (>80%)
- High error rate (>1%)
- App crashes

### Sentry Alerts

Configure in Sentry:
- New errors
- Error spikes
- Performance degradation

### Custom Alerts with Webhooks

**Create webhook handler:**

```python
@app.post("/webhooks/alerts")
async def receive_alert(alert: dict):
    # Send to Slack, Discord, PagerDuty, etc.
    await send_notification(alert)
    return {"status": "received"}
```

**Slack integration:**

```python
import httpx

async def send_slack_alert(message: str):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={
            "text": f"🚨 AniList GPT Alert: {message}"
        })
```

---

## 📊 Dashboards

### Key Metrics Dashboard

Create a dashboard showing:

1. **Requests/minute**
2. **Average response time**
3. **Error rate %**
4. **Cache hit rate**
5. **Active connections**
6. **Top searched anime**
7. **Tool usage breakdown**

### Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "AniList GPT Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

---

## 🔍 Log Management

### Structured Logging

**Already configured in the app using structlog!**

View logs:
```bash
# Real-time logs
fly logs --app anilist-gpt

# Follow logs
fly logs --app anilist-gpt --follow

# Search logs
fly logs --app anilist-gpt | grep "ERROR"
```

### Log Aggregation (Optional)

**Ship logs to external service:**

```bash
# Using Vector (deploy alongside app)
fly deploy --config vector.toml
```

**Vector configuration:**

```toml
[sources.fly_logs]
type = "exec"
command = ["fly", "logs", "--app", "anilist-gpt"]

[sinks.datadog]
type = "datadog_logs"
inputs = ["fly_logs"]
api_key = "${DATADOG_API_KEY}"
```

---

## 📱 Mobile Notifications

### Setup PagerDuty Integration

```python
@app.exception_handler(Exception)
async def handle_exception(request, exc):
    # Log to Sentry
    sentry_sdk.capture_exception(exc)
    
    # Send PagerDuty alert for critical errors
    if isinstance(exc, CriticalError):
        await send_pagerduty_alert(exc)
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

## 🔄 Automated Monitoring Checks

### GitHub Actions Monitoring

Add to `.github/workflows/monitor.yml`:

```yaml
name: Health Check

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check production health
        run: |
          curl -f https://anilist-gpt.fly.dev/health || exit 1
      
      - name: Check database health
        run: |
          curl -f https://anilist-gpt.fly.dev/health/db || exit 1
      
      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {"text": "🚨 AniList GPT health check failed!"}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 📋 Monitoring Checklist

### Pre-Launch
- [ ] Health check endpoint responding
- [ ] Error tracking configured
- [ ] Log aggregation setup
- [ ] Alert thresholds configured
- [ ] Dashboard created
- [ ] On-call rotation established

### Post-Launch
- [ ] Monitor error rates for 24 hours
- [ ] Check performance metrics
- [ ] Verify cache hit rates
- [ ] Review user activity logs
- [ ] Adjust alert thresholds
- [ ] Document runbooks

---

## 🎯 Performance Benchmarks

**Target SLAs:**
- Response Time (p95): < 500ms
- Response Time (p99): < 1000ms
- Error Rate: < 0.1%
- Uptime: 99.9%
- Cache Hit Rate: > 80%

**Monitor These Weekly:**
- Average response time trends
- Error rate patterns
- Database query performance
- Cache effectiveness
- Resource utilization
