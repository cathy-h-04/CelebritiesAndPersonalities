# TODO: clean up and determine which packages are actually necessary

import os

import sqlite3
from sqlite3 import Error

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from tempfile import mkdtemp

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# importing helper functions
from helpers import apology, login_required

import json

import pip._vendor.requests 

from flask_session import Session
#from tempfile import mkdtemp
#app = Flask(__name__)

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect("os.path.basename(celebs.db)")
        #connection = sqlite3.connect("/Users/pzhang/Desktop/CS_Final_Project/CelebritiesAndPersonalities/celebs.db")
        print("Connection to SQLite DB successful")
    except Error as e:
        print("The error occurred")

    return connection

connection = create_connection("E:\\celebs.db")
connection2 = sqlite3.connect("users.db")

db = connection.cursor()
db2 = connection2.cursor()

db.execute("DROP TABLE celebs")

db.execute("CREATE TABLE if not exists celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")
# db.execute("CREATE TABLE celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")
db2.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, maiden TEXT NOT NULL, nickname TEXT NOT NULL)")

# TODO: create a third table in which a user's top 20 matches are stored (include name as foreign key, celeb names, and percent matches)
celebs = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
characters = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])
character_data = (characters.json()["profiles"])

data = celeb_data + character_data

# Configure application
app = Flask(__name__)

# TODO: look into using custom filters with jinja if desired
    # this filter was added for finance: app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# TODO: configure this for our database as necessary (not sure if this is okay or if we need change)
#db = SQL("sqlite:///celebs.db")

# # TODO: This code in finance makes sure API key is set, so we may want similar code
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
def index():

    return render_template("index.html")


# TODO: adjust to what we want here (I think about is a static page though)
@app.route("/about", methods=["GET"])
#@app.route("/about", methods=["GET", "POST"])
def about():
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("about.html")

@app.route("/methodology", methods=["GET"])
def methodology():
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("methodology.html")
    


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
        rows = db2.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


# @app.route("/test", methods=["GET", "POST"])
# @login_required
# def test():

#     if request.method == "POST":        
#         # declaring each user's input as variables
#         mbti = request.form.get("mbti")
#         enne = request.form.get("enne")
#         name = request.form.get("name")
        
#         # declaring each user's ratings as variables
#         mbti_rating = request.form.get("mbti_rating")
#         enne_rating = request.form.get("enne_rating")
#         name_rating = request.form.get("name_rating")
        
#         # User initial api information
#         nationality = pip._vendor.requests.get('https://api.nationalize.io/?name='+name)
#         gender = pip._vendor.requests.get('https://api.genderize.io/?name='+name)
#         age = pip._vendor.requests.get('https://api.agify.io/?name='+name)

#         # user-specific ai-generated nationality, gender, and age
#         user_nat = (nationality.json()['country'][0])['country_id']
#         user_gen = gender.json()['gender']
#         user_age = age.json()['age']

#         db.execute("SELECT * FROM celebs")
    
        
#         celeb_count = db.execute("SELECT count(id) FROM celebs")
        
#         for i in range(celeb_count):
#             points = 0
#             celeb_enne = 0
#             celeb_mbti = 0
#             celeb_count = 0
            
#             celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", i)
#             for i in range(0, 3):
#                 if celeb_mbti[i] == mbti[i]:
#                     points += 0.25 * mbti_rating 
                 
            
#             celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", i)
            
#             if celeb_enne[0] == enne:
#                 points += enne_rating

#             celeb_name = db.execute("SELECT name FROM celebs WHERE id = ?", i)
            
#             celeb_nationality_search = requests.get('https://api.nationalize.io/?name='+celeb_name)
#             celeb_gender_search = requests.get('https://api.genderize.io/?name='+celeb_name)
#             celeb_age_search = requests.get('https://api.agify.io/?name='+celeb_name)

#             # user-specific ai-generated nationality, gender, and age
#             celeb_nat = (celeb_nationality_search.json()['country'][0])['country_id']
#             celeb_gen = celeb_gender_search.json()['gender']
#             celeb_age = celeb_age_search.json()['age']
            
#             if celeb_nat == user_nat:
#                 points += 1/3 * name_rating
            
#             if celeb_gen == user_gen:
#                 points += 1/3 * name_rating
            
#             if celeb_age == user_age:
#                 points += 1/3 * name_rating
            
#             db.execute("UPDATE celebs SET points = ? WHERE id = ?", points, i)
#             #db.execute("INSERT INTO celebs(points) VALUES(?) WHERE id = ?", points, i)


#      # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("test.html")
    
    
    
    
@app.route("/test", methods=["GET", "POST"])
# @login_required
def test():
     
        # declaring each user's input as variables
    mbti = "INTJ"
    enne = 5
    name = "Cathy"
        
        # declaring each user's ratings as variables
    mbti_rating = 3
    enne_rating = 4
    name_rating = 5
    
    #    # declaring each user's input as variables
#         mbti = request.form.get("mbti")
#         enne = request.form.get("enne")
#         name = request.form.get("name")
        
#         # declaring each user's ratings as variables
#         mbti_rating = request.form.get("mbti_rating")
#         enne_rating = request.form.get("enne_rating")
#         name_rating = request.form.get("name_rating")
        
        # User initial api information
    nationality = pip._vendor.requests.get('https://api.nationalize.io/?name='+name)
    gender = pip._vendor.requests.get('https://api.genderize.io/?name='+name)
    age = pip._vendor.requests.get('https://api.agify.io/?name='+name)

        # user-specific ai-generated nationality, gender, and age
    user_nat = (nationality.json()['country'][0])['country_id']
    user_gen = gender.json()['gender']
    user_age = age.json()['age']
    
    celeb_count = 20
        
    for i in range(celeb_count):
        points = 0
        
        celeb_enne = 0
        celeb_mbti = 0
        celeb_count = 0
           
        celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i + 1,)).fetchone()[0]
        # celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", i)
        for i in range(0, 3):
            if celeb_mbti[i] == mbti[i]:
                points += 0.25 * mbti_rating 
                 
        celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i + 1,)).fetchone()[0]
        # celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", i)
            
        if celeb_enne[0] == enne:
            points += enne_rating

        celeb_name = db.execute("SELECT name FROM celebs WHERE id = ?", (i + 1,)).fetchone()[0]
        # celeb_name = db.execute("SELECT name FROM celebs WHERE id = ?", i)
            
        celeb_nationality_search = pip._vendor.requests.get('https://api.nationalize.io/?name='+celeb_name)
        celeb_gender_search = pip._vendor.requests.get('https://api.genderize.io/?name='+celeb_name)
        celeb_age_search = pip._vendor.requests.get('https://api.agify.io/?name='+celeb_name)

            # user-specific ai-generated nationality, gender, and age
        celeb_nat = (celeb_nationality_search.json()['country'][0])['country_id']
        celeb_gen = celeb_gender_search.json()['gender']
        celeb_age = celeb_age_search.json()['age']
            
        if celeb_nat == user_nat:
            points += 1/3 * name_rating
            
        if celeb_gen == user_gen:
            points += 1/3 * name_rating
            
        if celeb_age == user_age:
            points += 1/3 * name_rating
            
        db.execute("UPDATE celebs SET points = ? WHERE id = ?", points, i)
            #db.execute("INSERT INTO celebs(points) VALUES(?) WHERE id = ?", points, i)


     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("test.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    # TODO: consider whether using session.clear might be problematic since a user could misclick on a file
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
        # TODO: fix this implementation of the users database 
        rows = db2.execute("SELECT * FROM users WHERE username = ?", username)
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
        db2.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))

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
        rows = db2.execute("SELECT * FROM users WHERE username = ?", username)
        if check_password_hash(rows[0]["hash"], newpassword):
            return apology("Repeated password", 403)

        # update new password into database
        db2.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(newpassword), username)

    # redirect to login page
    return redirect("/login")


# TODO: Code Result page
# @app.route("/results", methods=["GET", "POST"])
# @login_required
# def results():
#     if request.method == "POST":        
#         # TODO: add code for results here as necessary

@app.route("/account", methods=["GET", "POST"])
# @login_required
def account():
    if request.method == "GET":
        return render_template("account.html")


#TODO copied from finance
# Personal Touch
@app.route("/changepass", methods=["GET", "POST"])
# @login_required
def changepass():
    """Change password"""
    # # user reached route via GET
    # session.clear()

    if request.method == "GET":
        return render_template("changepass.html")

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
    if request.method == "GET":
        return render_template("compatibility.html")

