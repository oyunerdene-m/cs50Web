import os

from flask import Flask, render_template, request
from models import *
from goodreadsapi import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get('passenger_name')
    flight_id = request.form.get('flight_id')

    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="Flight doesn't exist.")

    if not name:
        return render_template("error.html", message="Provide your name")
    
    # Add passenger
    # if we don't provide add_passenger function in Flight class
    # passenger = Passenger(name=name, flight_id=flight_id)
    # db.session.add(passenger)
    # db.session.commit()

    # if we added add_passenger method in Flight class:
    flight.add_passenger(name)
    
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def more(flight_id):
    flight = Flight.query.get(flight_id)
    print(aoi_book)
    if flight is None:
        return render_template("error.html", message="Flight doesn't exist.")

    # Get all passengers.
    #passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    # after set relations in models.py Flight class:
    passengers = flight.passengers
    

print(goodreadsapi.result)
    
    
        
    

