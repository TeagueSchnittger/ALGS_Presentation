from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from generator import generate_pool
from optimizer import optimize_system
from dungeons import DUNGEONS

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    seed = int(data.get("seed", 42))
    capacity = int(data.get("capacity", 25))
    pool = generate_pool(seed)
    return jsonify({"pool": pool, "seed": seed, "capacity": capacity})


@app.route("/api/dungeons", methods=["GET"])
def api_dungeons():
    summary = [{"id": d["id"], "name": d["name"], "description": d["description"]} for d in DUNGEONS.values()]
    return jsonify({"dungeons": summary})


@app.route("/api/dungeon/<int:dungeon_id>", methods=["GET"])
def api_dungeon(dungeon_id):
    d = DUNGEONS.get(dungeon_id)
    if not d:
        return jsonify({"error": "Dungeon not found"}), 404
    return jsonify(d)


@app.route("/api/optimize", methods=["POST"])
def api_optimize():
    data = request.json
    seed = int(data.get("seed", 42))
    capacity = int(data.get("capacity", 25))
    dungeon_id = int(data.get("dungeon_id", 1))

    dungeon = DUNGEONS.get(dungeon_id)
    if not dungeon:
        return jsonify({"error": "Dungeon not found"}), 404

    pool = generate_pool(seed)
    result = optimize_system(
        pool,
        capacity,
        dungeon["grid"],
        dungeon["start"],
        dungeon["goal"]
    )
    result["pool"] = pool
    result["seed"] = seed
    result["dungeon"] = dungeon
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
