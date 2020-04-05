import os

from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgresql:///postgres")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    flights = db.execute(
        "SELECT id, origin, destination, duration FROM flights").fetchall()

    return render_template("index.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    passenger_name = request.form.get('passenger_name')
    if not passenger_name:
        return render_template("error.html", message="Provide your name!")
    try:
        choosed_flight = int(request.form.get('flight_id'))
        passenger_name = request.form.get('passenger_name')
    except ValueError:
        return render_template("error.html", message="Invalid flight number or name")

    if db.execute(
            "SELECT * FROM flights WHERE id = :id", {"id": choosed_flight}).rowcount == 0:
        return render_template("error.html", message="Flight doesn't exist!")

    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id) ", {
               "name": passenger_name, "flight_id": choosed_flight})
    db.commit()

    return render_template("success.html")
