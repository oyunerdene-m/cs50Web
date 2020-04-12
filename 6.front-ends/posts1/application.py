from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/posts", methods=["POST"])
def posts():

  # start = request.form.get("start")
  # end = request.form.get("end")
  start = 1
  end = 10

  posts = []
  for i in range(start, end + 1):
    posts.append(f"Post #{i}")
  return jsonify(posts)
