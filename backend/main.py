from flask import Flask, request, jsonify
import json
import logging
import psutil
import GPUtil

app = Flask(__name__)

logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_system_info():

    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    gpus = GPUtil.getGPUs()
    gpu_usage = gpus[0].load * 100 if gpus else None

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "gpu": gpu_usage
    }

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the API"

@app.route("/api/metrics")
def metrics_api():
    return jsonify(load_data())


@app.route("/data", methods=["GET"])
def get_data():
    logging.info("GET /data requested")
    data = load_data()
    return jsonify(data), 200

@app.route("/index.js")
def serve_js():
    return (".", "index.js")


@app.route("/data", methods=["POST"])
def add_data():
    try:
        incoming_data = get_system_info()

        data = load_data()
        data.append(incoming_data)
        save_data(data)

        return jsonify({"message": "System stats saved"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)