from flask import Flask, render_template, request
import webbrowser
import threading
import os
import signal

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save_env():
    key = request.form["key"]
    value = request.form["value"]

    with open(".env", "a") as f:
        f.write(f"{key}={value}\n")

    return "Enregistrement réussi"

@app.route("/shutdown", methods=["POST"])
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return "Serveur arrêté"

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=False)


# To package
# python -m PyInstaller config.py ^
#   --noconsole --onefile ^
#   --distpath . ^
#   --workpath temp_build ^
#   --specpath temp_build
