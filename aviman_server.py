from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

FILE_DB = "member_data.json"
FILE_BAN = "banned.json"

app = Flask(__name__)
CORS(app)

# ---------------- UTILITIES ----------------

def load_users():
    if not os.path.exists(FILE_DB):
        return []
    with open(FILE_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(FILE_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def load_banned():
    if not os.path.exists(FILE_BAN):
        return []
    with open(FILE_BAN, "r", encoding="utf-8") as f:
        return json.load(f)

def save_banned(banned):
    with open(FILE_BAN, "w", encoding="utf-8") as f:
        json.dump(banned, f, indent=4)

# ---------------- USERS ----------------

@app.get("/users")
def get_users():
    return jsonify(load_users())

@app.post("/register")
def register():
    new_user = request.json
    users = load_users()
    users.append(new_user)
    save_users(users)
    return {"status": "ok"}

# ---------------- BAN SYSTEM ----------------

@app.post("/ban")
def ban_user():
    data = request.json
    banned = load_banned()

    entry = {
        "name": data.get("name", "").strip(),
        "type": data.get("type", "").strip().lower(),
        "value": data.get("value", "").strip(),
        "reason": data.get("reason", "").strip(),
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    banned.append(entry)
    save_banned(banned)

    return {"status": "banned"}

# ---------------- RUN (RENDER COMPATIBLE) ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
