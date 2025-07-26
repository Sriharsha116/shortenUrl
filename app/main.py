from flask import Flask, request, jsonify, redirect
from app.models import (
    save_url_mapping, get_original_url, increment_click, get_clicks, get_metadata
)
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route("/")
def health_check():
    return jsonify({"service": "URL Shortener API", "status": "healthy"})

@app.route("/shorten", methods=["POST"])
def shorten_url():
    try:
        data = request.get_json()
        original_url = data.get("url")

        if not original_url or not is_valid_url(original_url):
            return jsonify({"error": "Invalid URL"}), 400

        short_code = generate_short_code()

        # Save or update the mapping
        save_url_mapping(original_url, short_code)

        return jsonify({"short_code": short_code})
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": "Internal server error"}), 500

@app.route("/<short_code>")
def redirect_to_url(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        increment_click(short_code)
        return redirect(original_url)
    return jsonify({"error": "URL not found"}), 404

@app.route("/stats/<short_code>")
def get_stats(short_code):
    return jsonify({
        "clicks": get_clicks(short_code),
        "metadata": get_metadata(short_code)
    })


