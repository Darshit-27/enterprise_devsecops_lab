from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return "Enterprise DevSecOps Lab Running"


# ---------------------------
# SQL Injection Vulnerability
# ---------------------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        return f"Executing query: {query}"

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

    q = request.args.get("q")

    return f"Search results for: {q}"


# ---------------------------
# Command Injection
# ---------------------------
@app.route("/ping")
def ping():

    host = request.args.get("host")

    cmd = f"ping -c 1 {host}"

    output = subprocess.getoutput(cmd)

    return f"<pre>{output}</pre>"


# ---------------------------
# File Upload Vulnerability
# ---------------------------
@app.route("/upload", methods=["GET","POST"])
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

    file = request.args.get("file")

    path = f"./uploads/{file}"

    return send_file(path)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
