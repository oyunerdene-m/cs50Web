import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# A more useful application of this bottom-detection would be the dynamic 
# loading of more content when the bottom of a webpage has been reached.

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/posts", methods=["POST"])
def posts():

    # Get start and end point for posts to generate.
    start = int(request.form.get('start'))
    end = int(request.form.get('end'))
    
    # Generate list of posts.
    data = []
    for i in range(start, end+1):
      data.append(f"Post: #{i}")

    # Artificially delay speed of response.
    time.sleep(1)

    # Return list of posts.
    return jsonify(data)
