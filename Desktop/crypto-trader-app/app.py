from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Placeholder portfolio simulation
portfolio = {
    "cash": 5000.00,
    "positions": [],
    "history": []
}

KEYS_FILE = "keys.json"

def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    return None

def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        api_key = request.form["api_key"]
        api_secret = request.form["api_secret"]
        save_keys({"api_key": api_key, "api_secret": api_secret})
        return redirect(url_for("dashboard"))

    keys = load_keys()
    if not keys:
        return render_template("connect.html")
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    keys = load_keys()
    if not keys:
        return redirect(url_for("home"))

    summary = {
        "today": 43.21,
        "week": 118.90,
        "month": 295.67,
        "cash": portfolio["cash"],
        "open_positions": len(portfolio["positions"]),
        "trades": len(portfolio["history"]),
        "status": "Auto-Trading Enabled"
    }

    return render_template("index.html", summary=summary)

# 🔧 Required for Render.com
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))