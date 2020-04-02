import os
import datetime

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Check for environment variable
if not "postgresql:///books":
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///books"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("error.html", message="Please provide your name!")
        if not password:
            return render_template("error.html", message="Please provide your password!")

        #find user by name
        f_user = User.query.filter_by(name=username).first()
        if f_user != None:
            return render_template("error.html", message="User with that name exists!")
        
        user = User(name=username)
        password_hash = user.set_password(password)
       
        db.session.add(user)
        db.session.commit()

        isSigned=True
    
        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        #check if username matched in db
        username = request.form.get("username")
        password = request.form.get("password")

        found_user = User.query.filter_by(name=username).first()
        if found_user is None or (found_user.check_password(password) == False):
            return render_template("error.html", message="Username or password is incorrect!")

        session["user_id"] = found_user.id

        return redirect("/")
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    ## first search by title
    search = request.form.get("search")

    found_books = Book.query.filter(or_(Book.title.like('%' + search +'%'), 
                                        Book.isbn.like('%' + search +'%'), 
                                        Book.author.like('%' + search +'%'))).all()
   
    return render_template("books.html", books=found_books)


@app.route("/books/<int:book_id>")
def more(book_id):
    book = Book.query.get(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    #reviews = book.reviews

    return render_template("more.html", book=book, reviews=reviews)

@app.route("/review/new/<int:book_id>", methods=["GET", "POST"])
def add_review(book_id):
    if request.method == "GET":
        book = Book.query.get(book_id)
        return render_template("new.html", book=book) 
    else:
        book = Book.query.get(book_id)
        content = request.form.get("content")
        rating = int(request.form.get("rating"))
        current_time = datetime.now() 
        day = current_time.strftime("%Y-%m-%d (%H:%M:%S)")
        user_id = session["user_id"]
        
        review = Review(content=content, createdAt=day, rating=rating, user_id=user_id, book_id=book_id)
        db.session.add(review)
        db.session.commit()

        
        return redirect(url_for('more', book_id=book_id))


        


        









    





        

        
        

