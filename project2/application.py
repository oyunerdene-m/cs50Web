import os
import requests

from flask import Flask, render_template, request, redirect, jsonify, session
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

names = ["oyuka"]

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/get_names")
def get_names():
  return jsonify(names)

@socketio.on("add name")
def add(data):
    username = data["username"]
    print(names)
    if username in names:
      return "That name is already registered!"
    names.append(username)
    emit("announce names", {"username": username}, broadcast=True)  









if __name__ == '__main__':
  socketio.run(app)