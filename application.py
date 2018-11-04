import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import googlemaps
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

gmaps = googlemaps.Client(key='AIzaSyAtCmvDQ7BP5BjtjFlkCffXQnQJIo2bTEY')

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# DATABASE = "sqlite:///envice.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return str(self.username) + ", " + str(self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    mileage = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(100), nullable=False)
    miles = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return str(self.model) + ", " + str(self.year) + ", " + str(self.make) + ", " + str(self.result) + str(self.date_posted)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.String(100))
    mileage = db.Column(db.String(100))

    def __repr__(self):
        return str(self.make) + ", " + str(self.model) + ", " + str(self.year)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        userid = session["user_id"]

        # get data from html
        make = request.form.get("make")
        year = request.form.get("year")
        model = request.form.get("model")

        mileage = Car.query.filter_by(make=request.form.get("make"), year=request.form.get(
            "year"), model=request.form.get("model")).first()

        if not mileage:
            return apology("Car with make year and model not found", 400)

        mileage = mileage.first()

        # use google maps api to get miles
        miles = request.form.get("miles")

        # used google map api to get range of gas price in the area
        price = request.form.get("price")

        # Calculation based on miles and make model year info
        # price per gallon divided by mileage is how much per mile
        result = (float(price) / float(mileage)) * float(miles)

        userid = session["user_id"]
        post = Post(model=model,
                    year=year, make=make, mileage=mileage, miles=miles, price=price, result=result, user_id=userid)

        db.session.add(post)
        db.session.commit()
        print('success')

        return render_template("/result.html", model=model,
                               year=year, make=make, mileage=mileage, miles=miles, price=price, result=result)
    else:
        # make, model, year
        make = list(set([car.make for car in Car.query.all()]))
        make.sort()
        model = list(set([car.model for car in Car.query.all()]))
        model.sort()
        year = list(set([car.year for car in Car.query.all()]))
        year.sort()

        return render_template("index.html", make=make, model=model, year=year)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userid = session["user_id"]

    result = Post.query.filter_by(user_id=userid).all()

    return render_template("history.html", result=result)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(
            username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Esure email was submitted
        if not request.form.get('email'):
            return apology("Missing Email!", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("missing password", 400)

        # Ensure password was confirmed
        if not request.form.get("confirmation"):
            return apology("must reenter password", 400)

        # Ensure password and confirmation match
        entered_password = request.form.get("password")

        # Require password to be length seven with at least one number
        if len(entered_password) < 7:
            return apology("length of password must be at least 7")
        if not any(char.isdigit() for char in entered_password):
            return apology("must contain at least one number")

        confirmed_password = request.form.get("confirmation")
        if entered_password != confirmed_password:
            return apology("make sure your passwords match", 400)

        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Check if username already exists
        result = User.query.filter_by(
            username=request.form.get("username")).all()

        # print("hello")
        if result:
            return apology("username already exists", 400)

        # session["user_id"] = remember
        user = User(username=request.form.get("username"),
                    email=request.form.get('email'), password=hash)
        db.session.add(user)
        db.session.commit()
        print('success')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/location/<pos>", methods=["GET", "POST"])
def price(pos):
    req = Request('https://gasprices.aaa.com/?state='+pos, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
#    quote_page = ''
#    with urllib.request.urlopen(quote_page) as url:
#        page = url.read()
    soup = BeautifulSoup(webpage, 'html.parser')
    
    price_box = soup.findAll('p', attrs={'class':'numb'})[1]
    
    price = price_box.text

    return jsonify({'price' : price})



