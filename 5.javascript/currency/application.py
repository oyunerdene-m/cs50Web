import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')


@app.route("/convert", methods=["POST", "GET"])
def convert():
  if request.method == 'GET':
    return render_template('index.html')
  elif request.method == 'POST':
    currency = request.form.get("currency")
  
    res = requests.get("http://data.fixer.io/api/latest?", params={"access_key": "6ecf162da9b29cd2507bb70fb5fd6295", "base": "EUR", "symbols": currency})

    if res.status_code != 200:
      return jsonify({"success": False})

    data = res.json()
    #{'success': True, 'timestamp': 1586155747, 'base': 'EUR', 'date': '2020-04-06', 'rates': {'USD': 1.081906}}

    if currency not in data["rates"]:
      return jsonify({"success": False})

    return jsonify({"success": True, "rate": data['rates'][currency]})

  
