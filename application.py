import os

from flask import Flask, render_template, session, request, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Login", methods=["GET", "POST"])
def Login():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            return render_template("error.html", message="username is missing")
        elif not password:
            return render_template("error.html", message="password is missing")
        
        result = db.execute("SELECT password FROM user_info WHERE username = :username",
                          {"username": username}).fetchone()[0]
        
        if result == None or not check_password_hash(result, password):
            return render_template("error.html", message="invalid username and/or password")
        
        session["username"] = username
        
        return redirect("/search")
    
    else:
      return render_template("Login.html")
    

@app.route("/Register", methods=["GET", "POST"])
def Register():
    
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        if not username:
            return render_template("error.html", message="username is missing")
        Check = db.execute("SELECT * FROM user_info WHERE username = :a",
                        {"a":username}).fetchall()
        if Check:
            return render_template("error.html", message="username already exist")
        elif not password:
            return render_template("error.html", message="password is missing")
        elif not confirm:
            return render_template("error.html", message="confirmation is missing")
        elif password != confirm:
            return render_template("error.html", message="confirmation did not match password")
        
        password_hash = generate_password_hash(password)
        
        db.execute("INSERT INTO user_info (username, password) VALUES (:username, :password)",
                {"username":username, "password":password_hash})    
        
        db.commit()    
            
        flash('Account created')
        
        return redirect("/Login")

    else:  
        return render_template("Register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    
    if request.method == "POST":
        
        search = request.form.get("search")
        if not search:
            return render_template("search.html", message="search field is empty.")
        
        query = "%" + search + "%"
        
        query = query.title()
        
        result = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                            isbn LIKE :query OR \
                            title LIKE :query OR \
                            author LIKE :query LIMIT 15", {"query": query})
        
        if result.rowcount == 0:
            return render_template("search.html", message="No books are found")
        else:
            books = result.fetchall()
            return render_template("search.html", data=books)
    
    else:
        return render_template("search.html")


@app.route("/book/<isbn>", methods=['GET','POST'])
def book(isbn):
    if request.method == "POST":
        uername = session["username"]
        
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment")
        
        book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                          {"isbn": isbn}).fetchone()[0]
        
        check = db.execute("SELECT * FROM reviews WHERE username = :username AND book_id = :book_id",
                           {"username": uername, "book_id": book_id})

        if check.rowcount == 1:
            return render_template("error.html", message='You already submitted a review for this book')
        else:
            db.execute("INSERT INTO reviews (username, book_id, comment, rating) VALUES\
                (:uername, :book_id, :comment, :rating)", 
                {"uername": uername,"book_id": book_id, "comment": comment, "rating": rating})
            
            db.commit()
            flash('Review submitted')
            return redirect("/book/" + isbn)
    else:
        book_info = db.execute("SELECT isbn, title, author, year FROM books\
                               WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
        
        book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                             {"isbn": isbn}).fetchone()[0]
        reviews = db.execute("SELECT username, comment, rating \
                            FROM reviews \
                            WHERE book_id = :book_id",
                            {"book_id": book_id}).fetchall()
        
        return render_template("book.html", book_info=book_info, reviews=reviews)
        
