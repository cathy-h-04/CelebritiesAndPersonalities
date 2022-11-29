
import os

import sqlite3
from sqlite3 import Error

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# TODO: use a different hash or import what is necessary for this hash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# importing helper functions
from CelebritiesAndPersonalities.helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# TODO: look into using custom filters with jinja if desired
    # this filter was added for finance: app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# TODO: configure this for our database
db = SQL("sqlite:///finance.db")

# # TODO: This code in finance makes sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

# TODO: adjust this code below from finance pset to what we want
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# TODO: add any input necessary, although I don't think there is any necessary
@app.route("/")
# @login_required
def index():

    return render_template("index.html")


# TODO: adjust to what we want here (I think about is a static page though)
@app.route("/about", methods=["GET", "POST"])
def about():
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/test", methods=["GET", "POST"])
@login_required
def test():

    if request.method == "POST":
        # checking that user has inputted the three characteristics for assessment
        
        # declaring each user's input as variables
        mbti = request.form.get("mbti")
        enne = request.form.get("enne")
        astro = request.form.get("astro")
 
        if not mbti:
            return apology("Must input your myers-briggs type")

        if not enne:
            return apology("Must input your enneagram type")

        if not astro:
            return apology("Must input your astrological sign")

        if not mbti_rating:
            return apology("Must input your myers-briggs type")

        if not enne_rating:
            return apology("Must input your enneagram type")

        if not astro_rating:
            return apology("Must input your astrological sign")

        # declaring each user's ratings as variables
        mbti_rating = request.form.get("mbti_rating")
        enne_rating = request.form.get("enne_rating")
        astro_rating = request.form.get("astro_rating")

        # TODO: change this for loop so that it actually cycles through celebrities
        for celebrity in celebrities:
            for mbti in celebrity:
                 


     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmpassword")

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure username was submitted
        elif not username:
            return apology("must provide username", 400)

        # Checking that user has confirmed password
        elif not confirmation:
            return apology("must confirm password", 400)

        # Checking that username and password match
        elif password != confirmation:
            return apology("passwords must match", 400)

        # checking that username is unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists", 400)

        # Checking that the password has at least one digit, 1 special character, and 5 letters in their password
        digits = 0
        letters = 0
        special_characters = 0

        for char in password:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            else:
                special_characters += 1

        if letters < 5 or digits < 1 or special_characters < 1:
            return apology("Password must contain at least 5 letters, 1 digit, and 1 special character.")

        # 2nd personal touch, checks that password does not contain username
        elif password.find(username) != -1:
            return apology("Password must not contain username")

        # adding user's username and hashed password into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Confirm registration
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# TODO: !!!! may need to change route
@app.route("/passwordchange", methods=["GET", "POST"])
def passwordchange():
    """Change password"""
    # user reached route via GET
    session.clear()

    if request.method == "GET":
        return render_template("passwordchange.html")

    # user reached route via POST
    else:

        # make sure user inputs a password, username and confirms password
        if not username:
            return apology("Must provide username.")

        elif not newpassword:
            return apology("Must provide a new password.")

        elif not newconfirmation:
            return apology("Must confirm new password.")

        # get new password, password confirmation, & username
        username = request.form.get("username")
        newpassword = request.form.get("new_password")
        newconfirmation = request.form.get("new_confirmation")

        # check if old password equals new password
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if check_password_hash(rows[0]["hash"], newpassword):
            return apology("Repeated password", 403)

        # update new password into database
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(newpassword), username)

    # redirect to login page
    return redirect("/login")


# TODO: Code Result page
@app.route("/results", methods=["GET", "POST"])
@login_required
def results():


# TODO: Code Compatibility Page 
@app.route("/compatibility", methods=["GET", "POST"])
@login_required
def compatibility():

    if request.method == "POST":
        # checking that user has inputted the three characteristics for assessment
        
        # declaring each user's input as variables
        celeb = request.form.get("name")
        
        if not celeb:
            return apology("Must input a celebrity")

        #TODO: finish implementation of compatibility


# TODO: Code Test Page
