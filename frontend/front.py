from flask import Flask, session, redirect, render_template, request
import requests
import os
import logging

app = Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(
    filename="frontend.log",
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Frontend Flask server starting...")

app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_123")

from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    get_google_provider_cfg,
    CONTAINER_METRICS_URL
)

@app.route("/")
def index():
    if "user" not in session:
        logging.info("Unauthenticated user → redirecting to /login")
        return redirect("/login")

    try:
        host_response = requests.get("http://backend:5000/api/metrics", timeout=5)
        container_response = requests.get("http://backend:5000/api/container-metrics", timeout=5)

        metrics = host_response.json()
        containers = container_response.json()

        class Obj(dict):
            __getattr__ = dict.get

        metrics = Obj(metrics)
        containers = {name: Obj(stats) for name, stats in containers.items()}

        return render_template(
            "index.html",
            metrics=metrics,
            containers=containers
        )

    except Exception as e:
        logging.error(f"Frontend error: {e}")
        return f"Frontend error: {e}"

@app.route("/login")
def login():
    logging.info("User accessed /login → starting OAuth redirect")

    google_cfg = get_google_provider_cfg()
    auth_endpoint = google_cfg["authorization_endpoint"]

    request_uri = (
        f"{auth_endpoint}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )

    logging.debug(f"Redirecting user to Google OAuth: {request_uri}")
    return redirect(request_uri)

@app.route("/auth/callback")
def callback():
    logging.info("User returned to /auth/callback")

    code = request.args.get("code")
    logging.debug(f"Received OAuth code: {code}")

    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
    }

    logging.info("Requesting access token from Google...")
    token_response = requests.post(token_endpoint, data=token_data)
    tokens = token_response.json()

    if "access_token" not in tokens:
        logging.error(f"OAuth error: {tokens}")
        return "OAuth authentication failed. Check logs."

    logging.info("Access token received. Fetching user info...")
    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    userinfo_response = requests.get(
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )

    session["user"] = userinfo_response.json()
    logging.info(f"User logged in: {session['user']}")

    return redirect("/")

@app.route("/containers")
def show_container_metrics():
    if "user" not in session:
        return redirect("/login")

    logging.info("User accessed /containers")

    try:
        logging.info("Fetching container metrics...")
        metrics = requests.get(CONTAINER_METRICS_URL).json()

        logging.debug(f"Container metrics data: {metrics}")
        return render_template("containers.html", metrics=metrics)

    except Exception as e:
        logging.error(f"Error loading container metrics: {e}")
        return f"Error: {e}"

@app.route("/logout")
def logout():
    session.clear()
    logging.info("User logged out")
    return redirect("/login")

if __name__ == "__main__":
    logging.info("Starting Flask app on port 8000")
    app.run(host="0.0.0.0", port=8000)
