import os
import requests

from flask import Flask, jsonify, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.attributes import flag_modified

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
        elif not password:
            return render_template("error.html", message="Please provide your password!")

        #find user by name
        f_user = User.query.filter_by(name=username).first()
        if f_user:
            return render_template("error.html", message="User with that name exists!")
        
        user = User(name=username)
        password_hash = user.set_password(password)
    
        db.session.add(user)
        db.session.commit()

        flash("You successfully signed up")
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

        if not username:
            return render_template("error.html", message="Provide your username!", isRegistered=True)
        elif not password:
            return render_template("error.html", message="Provide your password!", isRegistered=True)

        found_user = User.query.filter_by(name=username).first()

        if found_user is None or (found_user.check_password(password) == False):
            return render_template("error.html", message="Invalid username or password!", isRegistered=True)

        #to remember which user is logged in
        session["user_id"] = found_user.id
        session["username"] = found_user.name
        flash("You successfully logged in", "success")
        return redirect("/")
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    # search by title, isbn, author
    search = request.form.get("search")

    if not search:
        flash("Provide your search text!", "error")
        return redirect('/')
    
    
    found_books = Book.query.filter(or_(Book.title.ilike('%' + search +'%'), 
                                        Book.isbn.ilike('%' + search +'%'), 
                                        Book.author.ilike('%' + search +'%'))).all()

    if len(found_books) == 0:
        flash("Sorry, there is no matching book!", "error")
        return redirect('/')
   
    return render_template("books.html", books=found_books)


@app.route("/books/<int:book_id>")
def more(book_id):
    noReviews = False

    book = Book.query.get(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    
    isbn = book.isbn

    #goodreads api info
    # res =  requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "aSHhhnXKPm2y1aV2Uhb8Q", "isbns": isbn})
    # result = res.json()
    #api_book_info = result['books'][0]
    api_book_info={
        'work_ratings_count': 5,
        'average_rating': 4.0
    }
    
    if not book:
        flash("Sorry, there's no info about this book")
        return redirect("search")

    elif not reviews:
        noReviews=True


    return render_template("more.html", book=book, reviews=reviews, api_book_info=api_book_info, noReviews=noReviews)
    
   
@app.route("/review/new/<int:book_id>", methods=["GET", "POST"])
def add_review(book_id):
    user_id = session["user_id"]
    
    if request.method == "GET":
        reviews = Review.query.filter(and_(Review.user_id==user_id, Review.book_id==book_id)).all()

        if len(reviews) > 0:
            flash("Sorry, you wrote your review on this book, but you can update that.")
            return redirect(url_for('more', book_id=book_id))
            

        book = Book.query.get(book_id)
        return render_template("new.html", book=book) 
    else:
        book = Book.query.get(book_id)

        content = request.form.get("content")
        rating = request.form.get("rating")

        if not content:
            flash("Provide your opinion!")
            return redirect(url_for('add_review', book_id=book_id))
        
        elif not rating:
            flash("Provide your rating!")     
            return redirect(url_for('add_review', book_id=book_id)) 
        
        review = Review(content=content, rating=rating, user_id=user_id, book_id=book_id)
        db.session.add(review)
        db.session.commit()

        return redirect(url_for('more', book_id=book_id))


@app.route("/books/<int:book_id>/review/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id, book_id):
    review = Review.query.get(review_id)
    book = Book.query.get(book_id)
    if request.method == "GET":
        return render_template("edit.html", review=review, book=book)
    else:
        new_content = request.form.get("old_content")
        new_rating = request.form.get("old_rating")

        review.content = new_content
        review.rating = new_rating
        db.session.commit()

        return redirect(url_for('more', book_id=book_id))


@app.route("/api/books/<isbn>")
def book_api(isbn):
    
    #book = db.execute("SELECT * FROM books WHERE isbn = ?", isbn=isbn)
    book = Book.query.filter_by(isbn=isbn).first()
   
    if not book:
        return jsonify({"error": "Invalid flight id."}), 422
    
    #goodreads api info
    res =  requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "aSHhhnXKPm2y1aV2Uhb8Q", "isbns": isbn})
    result = res.json()
    api_book_info = result['books'][0]

    #reviews = db.execute("SELECT * FROM reviews WHERE book_id=?", book_id=book.id)
    reviews = Review.query.filter_by(book_id=book.id).all()
    rev_count = len(reviews)

    return jsonify({
        "title": book.title,      
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "ratings": api_book_info['work_ratings_count'],
        "average_score": api_book_info['average_rating'],
        "review_count": rev_count
    })


        


        









    





        

        
        

