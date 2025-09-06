from flask import Flask, request, jsonify
from flask_cors import CORS  # allows frontend connection
import os

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

# In-memory counters for dashboard stats
stats = {"phishing": 0, "safe": 0}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Check if JSON contains 'url'
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400

    url = data["url"]

    # Additional check: URL should not be empty
    if not url.strip():
        return jsonify({"error": "URL is empty"}), 400

    # Dummy logic for testing
    if "https" in url.lower():
        prediction = "Safe"
        stats["safe"] += 1
    else:
        prediction = "Phishing"
        stats["phishing"] += 1

    return jsonify({"prediction": prediction})

@app.route("/stats", methods=["GET"])
def get_stats():
    total = stats["phishing"] + stats["safe"]
    phishing_pct = (stats["phishing"] / total) * 100 if total else 0
    safe_pct = (stats["safe"] / total) * 100 if total else 0

    return jsonify({
        "phishing": round(phishing_pct, 2),
        "safe": round(safe_pct, 2),
        "total": total
    })

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)