from flask import Flask
import json
import logging
import psutil

# Try loading GPU stats
try:
    import GPUtil
except ImportError:
    GPUtil = None


# Logging configuration
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_FILE = "data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            logging.info("Loaded data from file")
            return data

    except FileNotFoundError:
        logging.warning("data.json not found, returning empty list")
        return []

    except json.JSONDecodeError:
        logging.error("data.json is empty or corrupted, returning empty list")
        return []

    except Exception as e:
        logging.error(f"Unexpected error loading data: {e}")
        return []


def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            logging.info("Data saved to file successfully")

    except Exception as e:
        logging.error(f"Error saving file: {e}")


def get_system_info():
    logging.info("Collecting system info")

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    logging.info(f"CPU Usage: {cpu_usage}% | RAM Usage: {memory_usage}%")

    gpu_usage = 0
    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = round(gpus[0].load * 100, 2)
                logging.info(f"GPU Usage: {gpu_usage}%")
        except Exception as e:
            logging.error(f"GPU monitoring failed: {e}")

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "gpu": gpu_usage,
    }


def calculate_cpu_percent(stats):
    """Convert Docker raw CPU stats into percentage."""
    try:
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]

        if cpu_delta > 0 and system_delta > 0:
            num_cpus = len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])
            cpu_percent = (cpu_delta / system_delta) * num_cpus * 100.0
            return round(cpu_percent, 2)
    except Exception as e:
        logging.error(f"CPU percent calculation failed: {e}")

    return 0.0


def get_container_stats():
    logging.info("Container stats requested, but Docker not implemented yet")
    return {}
