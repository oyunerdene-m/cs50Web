import os
import csv

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origin, destination, duration in reader:
        # db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
        #            {"origin": origin, "destination": destination, "duration": duration})
        flight = Flight(origin=origin, destination=destination,
                        duration=duration)
        db.session.add(flight)
        print(
            f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    db.session.commit()


if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()
