import os
import json
import requests


SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_123")

# Google OAuth settings
GOOGLE_CLIENT_ID = "257315684530-1n51dejnqlk97s9g260bk9dt2c0pad6f.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/callback"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


API_BASE = os.environ.get("API_BASE", "http://backend:5000")
METRICS_URL = f"{API_BASE}/api/metrics"
CONTAINER_METRICS_URL = f"{API_BASE}/api/container-metrics"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
