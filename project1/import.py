import os
import csv

from flask import Flask
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///books"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn, title, author, year in reader:
    book = Book(isbn=isbn, title=title, author=author, year=year)

    db.session.add(book)
  db.session.commit()


if __name__ == "__main__":
  # Allows for command line interaction with Flask application
  with app.app_context():
      main()