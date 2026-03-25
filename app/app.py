from flask import Flask, request, send_file
import os
import subprocess
import logging
import psycopg2
from markupsafe import escape

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def log_attack(ip, endpoint, attack_type, payload, severity="HIGH"):
    logging.warning(
        f"[{severity}] {attack_type} | IP={ip} | Endpoint={endpoint} | Payload={payload}"
    )

# ---------------------------
# Log every request (TRACE)
# ---------------------------
@app.before_request
def log_request_info():
    ip = get_ip()
    logging.info(
        f"IP={ip} | METHOD={request.method} | PATH={request.path} | ARGS={request.args}"
    )

# ---------------------------
# DB Connection
# ---------------------------
def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="vulndb",
        user="admin",
        password="admin123"
    )

# ---------------------------
# Home
# ---------------------------
@app.route("/")
def home():
    return "Enterprise DevSecOps Lab Running"

# ---------------------------
# SQL Injection (VULNERABLE)
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    ip = get_ip()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Detect SQL Injection
        if "'" in username or "OR" in username.upper():
            log_attack(ip, "/login", "SQL Injection", username)

        conn = get_db_connection()
        cur = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cur.execute(query)
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            return "Login SUCCESS (Vulnerable)"
        else:
            return "Login FAILED"

    return """
    <h2>Vulnerable Login</h2>
    <form method="POST">
    Username: <input name="username"><br>
    Password: <input name="password"><br>
    <button type="submit">Login</button>
    </form>
    """

# ---------------------------
# SQL Injection (SECURE)
# ---------------------------
@app.route("/secure-login", methods=["GET", "POST"])
def secure_login():
    ip = get_ip()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(query, (username, password))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            return "Secure Login SUCCESS"
        else:
            return "Secure Login FAILED"

    return """
    <h2>Secure Login</h2>
    <form method="POST">
    Username: <input name="username"><br>
    Password: <input name="password"><br>
    <button type="submit">Login</button>
    </form>
    """

# ---------------------------
# XSS (VULNERABLE)
# ---------------------------
@app.route("/search")
def search():
    ip = get_ip()
    q = request.args.get("q", "")

    if "<script>" in q:
        log_attack(ip, "/search", "XSS Attack", q)

    return f"Search results for: {q}"

# ---------------------------
# XSS (SECURE)
# ---------------------------
@app.route("/secure-search")
def secure_search():
    q = request.args.get("q", "")
    return f"Search results for: {escape(q)}"

# ---------------------------
# Command Injection
# ---------------------------
@app.route("/ping")
def ping():
    ip = get_ip()
    host = request.args.get("host", "")

    if ";" in host or "&&" in host:
        log_attack(ip, "/ping", "Command Injection", host)

    cmd = f"ping -c 1 {host}"
    output = subprocess.getoutput(cmd)

    return f"<pre>{output}</pre>"

# ---------------------------
# File Upload
# ---------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        return f"File saved to {path}"

    return """
    <h2>Upload File</h2>
    <form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload</button>
    </form>
    """

# ---------------------------
# Directory Traversal
# ---------------------------
@app.route("/download")
def download():
    ip = get_ip()
    file = request.args.get("file", "")

    if "../" in file:
        log_attack(ip, "/download", "Directory Traversal", file)

    path = f"./uploads/{file}"
    return send_file(path)

# ---------------------------
# View Logs
# ---------------------------
@app.route("/logs")
def view_logs():
    try:
        with open("security.log", "r") as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except:
        return "No logs yet"

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
