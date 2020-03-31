from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  password_hash = db.Column(db.String(128))
  reviews = db.relationship("Review", backref="user", lazy=True)
  reviewed_books = db.relationship("Book", backref="user", lazy=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Book(db.Model):
  __tablename__ = "books"
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String(128), nullable=False)
  title = db.Column(db.String(128), nullable=False)
  author = db.Column(db.String(128), nullable=False)
  year = db.Column(db.String, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  ##
  reviews = db.relationship("Review", backref="book", lazy=True)

  

class Review(db.Model):
  __tablename__ = "reviews"
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)
  createdAt = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
  rating = db.Column(db.Integer, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
  



