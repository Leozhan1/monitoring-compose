from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

from system_utils import (
    get_system_info,
    get_container_stats,
    load_data,
    save_data
)

logging.basicConfig(filename="api.log", level=logging.DEBUG, filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/")
def home():
    logging.info("Home endpoint accessed")
    return "Welcome to the API"


@app.route("/api/metrics")
def metrics_api():
    logging.info("GET /api/metrics")
    metrics = get_system_info()
    logging.debug(f"Metrics returned: {metrics}")
    return jsonify(metrics)


@app.route("/api/container-metrics")
def container_metrics():
    logging.info("GET /api/container-metrics")
    stats = get_container_stats()
    logging.debug(f"Container metrics: {stats}")
    return jsonify(stats)


@app.route("/data", methods=["GET"])
def get_data():
    logging.info("GET /data")
    data = load_data()
    logging.debug(f"Loaded {len(data)} entries")
    return jsonify(data), 200


@app.route("/data", methods=["POST"])
def add_data():
    logging.info("POST /data")
    try:
        new_stats = get_system_info()
        data = load_data()
        data.append(new_stats)
        save_data(data)

        logging.info("Saved new system stats entry")
        return jsonify({"message": "System stats saved"}), 201
    except Exception as e:
        logging.error(f"Error saving stats: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

