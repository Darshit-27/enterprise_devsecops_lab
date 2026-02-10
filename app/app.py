from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def home():
    return "Enterprise DevSecOps Vulnerable App"

@app.route("/users")
def users():
    username = request.args.get("username")

    conn = get_db()
    cur = conn.cursor()

    # ❌ VULNERABLE CODE (SQL Injection)
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    cur.execute(query)

    results = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(results)

"""
# ✅ SECURE CODE (COMMENTED – FOR REPORT & FIX PHASE)

query = "SELECT id, username, email FROM users WHERE username = %s"
cur.execute(query, (username,))
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
