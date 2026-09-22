from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "application": "EKS Demo Backend",
        "status": "running",
        "version": os.getenv("APP_VERSION", "2.0")
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/products")
def products():
    return jsonify({
        "products": [
            {"id": 1, "name": "Laptop", "price": 70000},
            {"id": 2, "name": "Mobile", "price": 30000},
            {"id": 3, "name": "Headphones", "price": 5000}
        ]
    })

@app.route("/api/cpu-test")
def cpu_test():
    total = 0
    for i in range(20_000_000):
        total += i * i

    return {"status": "done", "result": total}

@app.route("/api/config-check")
def config_check():
    return jsonify({
        "db_username_loaded": bool(os.getenv("DB_USERNAME")),
        "db_password_loaded": bool(os.getenv("DB_PASSWORD")),
        "api_key_loaded": bool(os.getenv("API_KEY"))
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6010)
