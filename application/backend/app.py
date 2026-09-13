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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6010)
