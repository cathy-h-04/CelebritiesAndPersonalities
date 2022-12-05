
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

from pip._vendor import requests

from flask_session import Session
#from tempfile import mkdtemp
#app = Flask(__name__)

import sqlite3
from sqlite3 import Error

# def create_connection(path):
#     connection = None
#     try:
#         connection = sqlite3.connect("os.path.basename(database.db)")
#         print("Connection to SQLite DB successful")
#     except Error as e:
#         print("The error occurred")

#     return connection

# connection = create_connection("E:\\database.db")

#ASK WHETHER THIS IS OKAY
connection = sqlite3.connect("database.db", check_same_thread=False)

# connection2 = sqlite3.connect("users.db")
# connection3 = sqlite3.connect("points.db")

db = connection.cursor()
# db2 = connection2.cursor()
# db3 = connection3.cursor()

# CREATE TABLE celebs (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#                 name TEXT NOT NULL, 
#                 MBTI TEXT NOT NULL, 
#                 enne TEXT NOT NULL
#             );



# CREATE TABLE users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#                 email TEXT NOT NULL, 
#                 password TEXT NOT NULL, 
#                 maiden TEXT NOT NULL, 
#                 nickname TEXT NOT NULL
#             );



# CREATE TABLE points (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                 celeb_id INTEGER NOT NULL,
#                 user_id INTEGER NOT NULL,
#                 points NUMERIC,
#                 FOREIGN KEY(celeb_id) REFERENCES celebs(id),
#                 FOREIGN KEY(user_id) REFERENCES users(id)
#             );

#db.execute("DROP TABLE celebs")

#db.execute("CREATE TABLE if not exists celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")
# db.execute("CREATE TABLE celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")
#db2.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, maiden TEXT NOT NULL, nickname TEXT NOT NULL)")


#BEFORE RUNNING:
db.execute("DELETE FROM points")
db.execute("DELETE FROM sqlite_sequence where name='points'")
# DELETE FROM points;
# DELETE FROM sqlite_sequence where name='points';
    
# TODO: create a third table in which a user's top 20 matches are stored (include name as foreign key, celeb names, and percent matches)
celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
characters = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])
character_data = (characters.json()["profiles"])

data = celeb_data + character_data


#QUESTION: SHOULD I JUST RUN THIS IN SQLITE?
# for person in data:
#     person_name = person["mbti_profile"]
#     person_personality = person["personality_type"]
#     mbti = person_personality.split()[0]
#     enne = person_personality.split()[1]
#     #print(person_name,mbti,enne)

#     db.execute("INSERT INTO celebs (name, MBTI, enne) VALUES (?, ?, ?)", (person_name, mbti, enne))
#     connection.commit()


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
    

def forgotpass():
    """Forgot password"""

    if request.method == "GET":
        return render_template("forgotpass.html")

    # user reached route via POST
    else:

        # get new password, password confirmation, & email
        email = request.form.get("email")
        newpass = request.form.get("newpass")
        confirmpass = request.form.get("confirmpass")
        securityques1 = request.form.get("securityques1")
        securityques2 = request.form.get("securityques2")


        # make sure user input's a password, email and confirms password
        if not email:
            return apology("Must provide email.")

        elif not newpass:
            return apology("Must provide a new password.")

        elif not confirmpass:
            return apology("Must confirm new password.")

        elif not securityques1:
            return apology("Must confirm new password.")

        elif not securityques2:
            return apology("Must confirm new password.")

        # check if old password equals new password
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if check_password_hash(rows[0]["hash"], newpass):
            return apology("Repeated password", 403)

        # update new password into database
        db.execute("UPDATE users SET hash = ? WHERE email = ?", (generate_password_hash(newpass), email))
        connection.commit()

    # redirect to login page
    return redirect("/login")



@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get User Input
        email = request.form.get("email")
        password = request.form.get("password")

        # # Ensure email was submitted
        # if not email:
        #     return apology("must provide email", 403)

        # # Ensure password was submitted
        # elif not password:
        #     return apology("must provide password", 403)
        print(email)
        print(password)

        # Query database for email
        # rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()[0]
        # rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()[0]
        
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()[0]
        
        print("THIS IS WHAT ROWS IS:", rows)
        
        #rows = db.execute("SELECT * FROM users").fetchall()
        
        #print(len(rows))
        
        #print(db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall())
        # print(db.execute("SELECT * FROM users WHERE email = ?", email))
        # rows = db.execute("SELECT * FROM users 
        # WHERE email = ?", email)
        # row = db.fetchone()

        # while rows is not None:
        #     print(rows)
        #     rows = db.fetchone()
        
        # TODO: implement this!!
        # Ensure email exists and password is correct
        #if len(rows) != 5
        
        if len(rows) == 0 or not check_password_hash(rows[2], password):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]
        session["user_id"] = rows[0]
        

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
    
        # declaring each user's input as variables
        mbti = request.form.get("MBTIs")
        print("MBTI", mbti)
        enne = request.form.get("ENNEs")
        print("ENNE", enne)
        name = request.form.get("firstname")
        print("NAME", name)
        
        # declaring each user's ratings as variables
        mbti_rating = int(request.form.get("mbtioptions"))
        print("MBTI RATING", mbti_rating)
        enne_rating = int(request.form.get("enneoptions"))
        print("ENNE RATING", enne_rating)
        name_rating = int(request.form.get("nameoptions"))
        print("NAME RATING", name_rating)
        
        # total_points = mbti_rating + enne_rating + name_rating
        
            
            # User initial api information
        nationality = requests.get('https://api.nationalize.io/?name='+name)
        gender = requests.get('https://api.genderize.io/?name='+name)
        age = requests.get('https://api.agify.io/?name='+name)

            # user-specific ai-generated nationality, gender, and age
        user_nat = (nationality.json()['country'][0])['country_id']
        user_gen = gender.json()['gender']
        user_age = age.json()['age']
                
                
        # print("THIS IS THE SESSION: "+ str(session["user_id"]))
        for i in range(1, 11):
            points = 0
        
            celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_full_name = db.execute("SELECT name FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_name = celeb_full_name.split()[0]

            
            for j in range(0, 4):
                if celeb_mbti[j] == mbti[j]:
                    points += (0.25 * mbti_rating )
                    
            if int(celeb_enne[0]) == enne:
                points += enne_rating
                

            name_exists = True
            
            celeb_gender_search = requests.get('https://api.genderize.io/?name='+celeb_name)
            celeb_age_search = requests.get('https://api.agify.io/?name='+celeb_name)
            
            if celeb_gender_search.json()['count'] == 0:
                name_exists = False
            
            if name_exists:
                celeb_nationality_search = requests.get('https://api.nationalize.io/?name='+celeb_name)
                celeb_nat = (celeb_nationality_search.json()['country'][0])['country_id']
                celeb_gen = celeb_gender_search.json()['gender']
                celeb_age = celeb_age_search.json()['age']
                
                
                if celeb_nat == user_nat:
                    points += 1/3 * name_rating
                
                if celeb_gen == user_gen:
                    points += 1/3 * name_rating
                    
                if celeb_age < (user_age + 5) and celeb_age > (user_age - 5):
                    points += 1/3 * name_rating
                                
            db.execute("INSERT INTO points (celeb_id, user_id, points) VALUES (?, ?, ?)", (i, session["user_id"], points))
        connection.commit()

            
        return redirect("/results")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("test.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    # TODO: consider whether using session.clear might be problematic since a user could misclick on a file
    session.clear()
    
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        email = request.form.get("email")
        print(email)
        password = request.form.get("password")
        print(password)
        confirmation = request.form.get("confirmpassword")
        securityques1 = request.form.get("securityques1")
        print(securityques1)
        securityques2 = request.form.get("securityques2")
        print(securityques2)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure email was submitted
        elif not email:
            return apology("must provide email", 400)

        # Checking that user has confirmed password
        elif not confirmation:
            return apology("must confirm password", 400)
        
        elif not securityques1:
            return apology("Must confirm new password.")

        elif not securityques2:
            return apology("Must confirm new password.")

        # Checking that email and password match
        elif password != confirmation:
            return apology("password and confirmation password must match", 400)


        # # Checking that the password has at least one digit, 1 special character, and 5 letters in their password
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

        # # 2nd personal touch, checks that password does not contain email
        elif password.find(email) != -1:
            return apology("Password must not contain email")
        
        # checking that email is unique for the account
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        print("FIRST CHECK")
        if len(rows) > 0:
            return apology("email already exists", 400)

        # adding user's email and hashed password into database
        # print("CODE START")
        db.execute("INSERT INTO users (email, password, maiden, nickname) VALUES(?, ?, ?, ?)", (email, generate_password_hash(password), securityques1, securityques2))
        connection.commit()
        # print("CODE END")

        # Confirm registration
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("register.html")

# TODO: !!!! may need to change route
@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Change password"""
    # user reached route via GET
    session.clear()

    if request.method == "GET":
        return render_template("changepass.html")

    # user reached route via POST
    else:

        # get new password, password confirmation, & email
        email = request.form.get("email")
        newpassword = request.form.get("newpass")
        newconfirmation = request.form.get("repeatpass")
        
        # make sure user inputs a password, email and confirms password
        if not email:
            return apology("Must provide email.")

        elif not newpassword:
            return apology("Must provide a new password.")

        elif not newconfirmation:
            return apology("Must confirm new password.")

        # check if old password equals new password
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()[0]
        if check_password_hash(rows[0]["hash"], newpassword):
            return apology("Repeated password", 403)

        # update new password into database
        db.execute("UPDATE users SET hash = ? WHERE email = ?", (generate_password_hash(newpassword), email))
        connection.commit()

    # redirect to login page
    return redirect("/login")


# TODO: Code Result page
@app.route("/results")
@login_required
def results():    
    print("ID: "+ str(session["user_id"]))
    top10 = db.execute("SELECT celeb_id, user_id, name, MBTI, enne, points FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = ? ORDER BY points DESC LIMIT 11", (session["user_id"],))

    shortlist = []
    for row in top10:
        shortlist.append(row)
        
    print(shortlist)
    # for person in top10:
    #     print(person)
    return render_template("results.html", shortlist = shortlist)

# @app.route("/account", methods=["GET", "POST"])
# @login_required
# def account():
#     if request.method == "GET":
#         return render_template("account.html")


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
        
        return render_template("compatibility.html")

    #     #TODO: finish implementation of compatibility
    if request.method == "GET":
        return render_template("compatibility.html")