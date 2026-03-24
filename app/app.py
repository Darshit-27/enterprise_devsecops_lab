from flask import Flask, request, send_file
import os
import subprocess
import psycopg2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------------------
# Home Route
# ---------------------------
@app.route("/")
def home():
    return "<h2>Enterprise DevSecOps Lab Running</h2>"


# ---------------------------
# SQL Injection (REAL AUTH)
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ⚠️ Intentionally vulnerable query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        try:
            conn = psycopg2.connect(
                host="db",
                database="vulndb",
                user="admin",
                password="admin123"
            )

            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchone()

            cur.close()
            conn.close()

            if result:
                return "<h2 style='color:green;'>Login Successful</h2>"
            else:
                return "<h2 style='color:red;'>Invalid Credentials</h2>"

        except Exception as e:
            return f"<pre>{e}</pre>"

    return """
    <h2>Login</h2>
    <form method="POST">
    Username: <input name="username"><br>
    Password: <input name="password"><br>
    <button type="submit">Login</button>
    </form>
    """


# ---------------------------
# XSS Vulnerability
# ---------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"<h3>Search results for: {q}</h3>"


# ---------------------------
# Command Injection
# ---------------------------
@app.route("/ping")
def ping():
    host = request.args.get("host", "")

    cmd = f"ping -c 1 {host}"
    output = subprocess.getoutput(cmd)

    return f"<pre>{output}</pre>"


# ---------------------------
# File Upload Vulnerability
# ---------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return "No file uploaded"

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        return f"<h3>File saved to {path}</h3>"

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
    file = request.args.get("file", "")
    path = f"./uploads/{file}"
    return send_file(path)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
