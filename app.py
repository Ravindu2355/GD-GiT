from flask import Flask, render_template, request, jsonify
from threading import Thread, Lock
import json
import os
from uploader import run

app = Flask(__name__)
session_file = "session_data.json"
lock = Lock()

def save_session(data):
    with open(session_file, "w") as f:
        json.dump(data, f)

def load_session():
    if os.path.exists(session_file):
        with open(session_file) as f:
            return json.load(f)
    return {"progress": {}, "paused": False, "running": False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_upload():
    config = request.json
    session = load_session()
    if session.get("running"):
        return jsonify({"error": "Already running"}), 400
    session["progress"] = {}
    session["paused"] = False
    session["running"] = True
    save_session(session)
    thread = Thread(target=run, args=(config, session, save_session, lock))
    thread.start()
    return jsonify({"message": "Started"})

@app.route("/status")
def status():
    session = load_session()
    return jsonify(session)

@app.route("/stop")
def stop():
    session = load_session()
    session["paused"] = True
    save_session(session)
    return jsonify({"message": "Paused"})

@app.route("/continue")
def resume():
    session = load_session()
    session["paused"] = False
    save_session(session)
    return jsonify({"message": "Continued"})

@app.route("/reset")
def reset():
    if os.path.exists(session_file):
        os.remove(session_file)
    return jsonify({"message": "Reset"})