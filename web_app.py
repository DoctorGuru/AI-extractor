from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "output/data.json"
SELECTED_FILE = "output/selected_product.json"


def load_products():
    """Load products from JSON and filter only readable ones for UI."""
    if not os.path.isfile(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    filtered_data = {}
    for leaflet, products in raw_data.items():
        filtered_products = [
            p for p in products
            if p.get("readable", False) and p.get("name")
        ]
        filtered_data[leaflet] = filtered_products

    return filtered_data


@app.route("/")
def index():
    products_dict = load_products()
    return render_template("index.html", products_dict=products_dict)


@app.route("/api/products")
def api_products():
    return jsonify(load_products())


@app.route("/select_product", methods=["POST"])
def select_product():
    data = request.get_json()
    if data:
        os.makedirs(os.path.dirname(SELECTED_FILE), exist_ok=True)
        with open(SELECTED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400


if __name__ == "__main__":
    app.run(debug=True)
