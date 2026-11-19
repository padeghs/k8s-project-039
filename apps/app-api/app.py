import os
import socket
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "research_records.txt")
TZ_BKK = timezone(timedelta(hours=7))

def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("[INIT] Research Storage Initialized for Padegh Sangbusarakum (ID: 039)\n")

@app.route("/")
@app.route("/health")
@app.route("/api/health")
def health():
    ensure_storage()
    return jsonify({
        "status": "ok",
        "student": "Padegh Sangbusarakum",
        "id": "039",
        "pod": socket.gethostname(),
        "storage_file": DATA_FILE
    })

@app.route("/records", methods=["GET"])
@app.route("/api/records", methods=["GET"])
def get_records():
    ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    return jsonify({
        "served_by_pod": socket.gethostname(),
        "total_lines": len(lines),
        "records": lines
    })

@app.route("/records", methods=["POST"])
@app.route("/api/records", methods=["POST"])
def create_record():
    ensure_storage()
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    if not text:
        return jsonify({"error": "text field is required"}), 400

    pod_name = socket.gethostname()
    timestamp = datetime.now(TZ_BKK).strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [Pod: {pod_name}] {text}\n"

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    return jsonify({
        "message": "saved",
        "served_by_pod": pod_name,
        "entry": entry.strip()
    }), 201

@app.route("/raw", methods=["GET"])
@app.route("/api/raw", methods=["GET"])
def raw_text():
    ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype="text/plain; charset=utf-8")

if __name__ == "__main__":
    ensure_storage()
    app.run(host="0.0.0.0", port=5000)