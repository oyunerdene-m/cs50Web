import requests
from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
  currency = request.form.get("currency")

  res = requests.get("http://data.fixer.io/api/latest", params={"access_key": "6ecf162da9b29cd2507bb70fb5fd6295", "base": "EUR", "symbols": currency})

  # Make sure request succeeded
  if res.status_code != 200:
      return jsonify({"success": False})

  # Make sure currency is in response
  data = res.json()
  print(data)
  # if currency not in data["rates"]:
  #     return jsonify({"success": False})

  return jsonify({"success": True, "rate": data["rates"][currency]})


