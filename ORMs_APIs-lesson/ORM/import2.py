import os
import csv

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def main():
    f = open("passengers.csv")
    reader = csv.reader(f)
    for name, flight_id in reader:
      passenger = Passenger(name=name, flight_id=flight_id)
      db.session.add(passenger)

      print(f"Added passenger: {passenger.name}, with flight id: {passenger.flight_id}")
    db.session.commit()


if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()
