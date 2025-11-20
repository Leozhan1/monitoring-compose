from flask import Flask, render_template, redirect, request, session, url_for
import requests
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_123")

# Google OAuth settings
GOOGLE_CLIENT_ID = "257315684530-9fnh07ahusfd9o0tdimgs7aufk3fgbph.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Backend API URL (Docker Compose internal hostname)
API_URL = os.environ.get("API_URL", "http://backend:5001/api/metrics")

# ------------------------------------------------
# Google OAuth helper
# ------------------------------------------------
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# ------------------------------------------------
# Login Page
# ------------------------------------------------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    try:
        response = requests.get(API_URL, timeout=3)
        metrics = response.json()
    except Exception as e:
        metrics = {"error": str(e)}

    return render_template("index.html", metrics=metrics)

# ------------------------------------------------
# Login Route
# ------------------------------------------------
@app.route("/login")
def login():
    google_cfg = get_google_provider_cfg()
    auth_endpoint = google_cfg["authorization_endpoint"]

    request_uri = (
        f"{auth_endpoint}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )

    return redirect(request_uri)

# ------------------------------------------------
# OAuth Callback
# ------------------------------------------------
@app.route("/auth/callback")
def callback():
    code = request.args.get("code")

    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
    }

    token_response = requests.post(token_endpoint, data=token_data)
    tokens = token_response.json()

    # Fetch user info
    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    userinfo_response = requests.get(
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )

    session["user"] = userinfo_response.json()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
