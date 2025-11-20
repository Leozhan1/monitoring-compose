from flask import Flask, request, jsonify
import json
import logging
import psutil

# Try to import GPUtil (optional)
try:
    import GPUtil
except ImportError:
    GPUtil = None

app = Flask(__name__)

logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_FILE = "data.json"


def load_data():
    """Load saved system metrics from JSON."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    """Save system metrics list to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_system_info():
    """Collect CPU, RAM, and optional GPU usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # GPU fallback
    gpu_usage = None

    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = gpus[0].load * 100
        except Exception:
            gpu_usage = None

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "gpu": gpu_usage if gpu_usage is not None else 0  # fallback to 0
    }


@app.route("/", methods=["GET"])
def home():
    return "Welcome to the API"


@app.route("/api/metrics")
def metrics_api():
    """Return gathered metrics for frontend."""
    return jsonify(load_data())


@app.route("/data", methods=["GET"])
def get_data():
    logging.info("GET /data requested")
    return jsonify(load_data()), 200


@app.route("/data", methods=["POST"])
def add_data():
    """Collect fresh stats and save them."""
    try:
        new_stats = get_system_info()
        data = load_data()
        data.append(new_stats)
        save_data(data)

        return jsonify({"message": "System stats saved"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


