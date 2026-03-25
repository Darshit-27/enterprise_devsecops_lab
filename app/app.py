from flask import Flask, request, send_file
from markupsafe import escape
import os
import subprocess
import logging

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------------------
# LOGGING SETUP
# ---------------------------
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def detect_attack(input_data):
    attack_patterns = ["'", "--", ";", "<script>", "||", "&&"]
    for pattern in attack_patterns:
        if pattern in str(input_data):
            logging.warning(f"⚠️ Possible attack detected: {input_data}")
            return True
    return False


# ---------------------------
# HOME
# ---------------------------
@app.route("/")
def home():
    return "Enterprise DevSecOps Lab Running"


# ---------------------------
# SQL Injection (VULNERABLE)
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        logging.info(f"Login attempt: {username}")

        if detect_attack(username) or detect_attack(password):
            return "⚠️ Suspicious input detected!"

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return f"Executing query: {query}"

    return """
    <h2>Login (Vulnerable)</h2>
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

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Hardcoded validation (safe simulation)
        if username == "admin" and password == "password":
            return "✅ Login successful (Secure)"
        else:
            return "❌ Invalid credentials"

    return """
    <h2>Login (Secure)</h2>
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
    q = request.args.get("q")

    if detect_attack(q):
        return "⚠️ XSS attempt detected!"

    return f"Search results for: {q}"


# ---------------------------
# XSS (SECURE)
# ---------------------------
@app.route("/secure-search")
def secure_search():
    q = request.args.get("q")

    return f"Search results for: {escape(q)}"


# ---------------------------
# COMMAND INJECTION (VULNERABLE)
# ---------------------------
@app.route("/ping")
def ping():
    host = request.args.get("host")

    if detect_attack(host):
        return "⚠️ Command Injection detected!"

    cmd = f"ping -c 1 {host}"
    output = subprocess.getoutput(cmd)

    return f"<pre>{output}</pre>"


# ---------------------------
# FILE UPLOAD (VULNERABLE)
# ---------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)

        logging.info(f"File uploaded: {file.filename}")

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
# DIRECTORY TRAVERSAL (VULNERABLE)
# ---------------------------
@app.route("/download")
def download():
    file = request.args.get("file")

    if detect_attack(file):
        return "⚠️ Directory Traversal detected!"

    path = f"./uploads/{file}"
    return send_file(path)


# ---------------------------
# VIEW LOGS (VERY IMPORTANT)
# ---------------------------
@app.route("/logs")
def view_logs():
    try:
        with open("app.log", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "No logs found"


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
