from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection (intentionally simple)
def get_db():
    return psycopg2.connect(
        host="db",
        database="vulnapp",
        user="vulnuser",
        password="vulnpass"
    )

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    cur = conn.cursor()

    # ==================================================
    # ❌ VULNERABLE CODE (SQL Injection)
    # ==================================================
    # User input is directly concatenated into SQL query
    # Attacker payload example:
    # username: admin' OR '1'='1
    # password: anything
    query = f"""
        SELECT id, username
        FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """
    cur.execute(query)

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401


"""
==================================================
✅ SECURE CODE (COMMENTED – DO NOT RUN TOGETHER)
==================================================

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    cur = conn.cursor()

    # ✅ Use parameterized queries (prevents SQL injection)
    query = """
        SELECT id, username
        FROM users
        WHERE username = %s
        AND password = %s
    """
    cur.execute(query, (username, password))

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
