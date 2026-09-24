from flask import Flask, jsonify, request
import os
import time

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# Total HTTP requests
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

# HTTP request latency
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    latency = time.time() - request.start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(latency)

    return response


@app.route("/")
def home():
    return jsonify({
        "application": "EKS Demo Backend",
        "status": "running",
        "version": os.getenv("APP_VERSION", "2.0")
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/products")
def products():
    return jsonify({
        "products": [
            {"id": 1, "name": "Laptop", "price": 70000},
            {"id": 2, "name": "Mobile", "price": 30000},
            {"id": 3, "name": "Headphones", "price": 5000}
        ]
    })


@app.route("/api/config-check")
def config_check():
    return jsonify({
        "db_username_loaded": bool(os.getenv("DB_USERNAME")),
        "db_password_loaded": bool(os.getenv("DB_PASSWORD")),
        "api_key_loaded": bool(os.getenv("API_KEY"))
    })


@app.route("/api/cpu-test")
def cpu_test():
    total = 0

    for i in range(20_000_000):
        total += i * i

    return {
        "status": "done",
        "result": total
    }


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6010)