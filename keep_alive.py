from threading import Thread
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "`@Gemini Pro Multi-Modal` is online!"

def run():
    app.run(host = "0.0.0.0", port = 8080)

def keep_alive():
    task = Thread(target = run)
    task.daemon = True
    task.start()
