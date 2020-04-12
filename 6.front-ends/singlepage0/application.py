from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

texts = [
  "first: Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  "second: Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.",
  "third: The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested."
]

@app.route("/first")
def first():
  return texts[0]

@app.route("/second")
def second():
  return texts[1]


@app.route("/third")
def third():
  return texts[2]