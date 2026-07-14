from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return {"message": "Task Tracker API is running"}

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({"id": new_id, "title": title, "completed": False}), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT id, title, completed FROM tasks").fetchall()
    conn.close()

    tasks = [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def complete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"id": task_id, "completed": True})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

