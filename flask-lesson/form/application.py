from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/person", methods=["POST"])
def person():
    name = request.form.get("name")
    return render_template("person.html", name=name)
