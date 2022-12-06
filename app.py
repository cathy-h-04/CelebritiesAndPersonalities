
import os

#importing sqlite3 for database use
import sqlite3
from sqlite3 import Error

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session

from flask_session import Session
# from flask_session import Session
from tempfile import mkdtemp

# importing package for creating and checking password hashes
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# importing helper functions for apology message and requiring users to login to access page
from helpers import apology, login_required

import json

# importing requests
from pip._vendor import requests

# print(celeb_count)
connection = sqlite3.connect("database.db", check_same_thread=False)

db = connection.cursor()

# Declaring count of celebrities in our database, 338, as a global variable
CELEB_COUNT = 338

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    # rendering our home page
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
    
@app.route("/forgotpass", methods=["GET", "POST"])
def forgotpass():
    """Forgot password"""
    # Rendering forgotpassword page if get method
    if request.method == "GET":
        return render_template("forgotpass.html")

    # user reached route via POST
    else:

        # get user's inputted email, new password, password confirmation, and security answers
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

        # Checking that the password has at least one digit, 1 special character, and 5 letters in their password
        digits = 0
        letters = 0
        special_characters = 0

        for char in newpass:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            else:
                special_characters += 1

        if letters < 5 or digits < 1 or special_characters < 1:
            return apology("New password must contain at least 5 letters, 1 digit, and 1 special character.")

          # 2nd personal touch, checks that password does not contain email
        elif newpass.find(email) != -1:
            return apology("Password must not contain email")

        # check if old password equals new password
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        
        # checking to see whether the inputted email exists within the database
        if rows is None:
           return apology("invalid email address", 403)

        
        if check_password_hash(rows[2], newpass):
            return apology("Repeated password", 403)

        # check that user correctly inputted security question 1
        if rows[3] != securityques1:
           return apology("The answer to one or more security questions is incorrect", 403)
 
        if rows[4] != securityques2:
           return apology("The answer to one or more security questions is incorrect", 403)

        # update new password into database
        db.execute("UPDATE users SET password = ? WHERE email = ?", (generate_password_hash(newpass), email))
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

        # sellecet all information for thaht user given their inputted email name
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        
        if len(rows) == 0 or not check_password_hash(rows[0][2], password):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]
        session["user_id"] = rows[0][0]
        print("FIRST CHECK THIS IS THE SESSION", session["user_id"])
        

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
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
        
            # User initial api information
        gender = requests.get('https://api.genderize.io/?name='+name)
        age = requests.get('https://api.agify.io/?name='+name)

        name_exists = True
            
        print(gender.json())
        
        if gender.json()['count'] == 0:
            name_exists = False
        
        if name_exists:
            nationality = requests.get('https://api.nationalize.io/?name='+name)
            user_nat = (nationality.json()['country'][0])['country_id']
            user_gen = gender.json()['gender']
            user_age = age.json()['age']

        
        for i in range(1, CELEB_COUNT + 1):
            points = 0
        
            celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_full_name = db.execute("SELECT name FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_nat = db.execute("SELECT nationality FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_gen = db.execute("SELECT gender FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_age = int(db.execute("SELECT age FROM celebs WHERE id = ?", (i,)).fetchone()[0])

            
            for j in range(0, 4):
                if celeb_mbti[j] == mbti[j]:
                    points += (0.25 * mbti_rating )
                    
            if int(celeb_enne[0]) == enne:
                points += enne_rating
                
            if celeb_nat == user_nat:
                points += 1/3 * name_rating
            
            if celeb_gen == user_gen:
                points += 1/3 * name_rating
                
            if celeb_age < (user_age + 5) and celeb_age > (user_age - 5):
                points += 1/3 * name_rating
            
            print(i, session["user_id"], points)
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
            return apology("Must provide password", 400)

        # Ensure email was submitted
        elif not email:
            return apology("Must provide email", 400)

        # Checking that user has confirmed password
        elif not confirmation:
            return apology("Must confirm password", 400)
        
        elif not securityques1:
            return apology("Must input the answer to first security question.")

        elif not securityques2:
            return apology("Must input the answer to second security question.")

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



@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Change password"""

    if request.method == "GET":
        return render_template("changepass.html")

    # user reached route via POST
    else:

        # get new password, password confirmation, & username
        email = request.form.get("email")
        oldpassword = request.form.get("old_password")
        newpassword = request.form.get("new_password")
        newconfirmation = request.form.get("new_confirmation")

        # make sure user inputs a password, username and confirms password
        if not email:
            return apology("Must provide email.")

        elif not oldpassword:
            return apology("Must provide the old password.")

        elif not newpassword:
            return apology("Must input new password.")

        elif not newconfirmation:
            return apology("Must input confirm new password.")

        # check if old password equals new password
        # rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        
        # checking to see whether the inputted email exists within the database
        if rows is None:
           return apology("invalid email address", 403)
       
        if check_password_hash(rows[2], newpassword):
            return apology("Repeated password", 403)
        
        # ensuring that old password matches the account specified
        if len(rows) == 0 or not check_password_hash(rows[2], oldpassword):
            return apology("invalid email and/or password", 403)

        # 2nd personal touch, checks that password does not contain email
        if newpassword.find(email) != -1:
            return apology("Password must not contain email")
        
        if oldpassword != newconfirmation:
           return apology("password and confirmation password must match", 400)

        # update new password into database
        db.execute("UPDATE users SET password = ? WHERE email = ?", (generate_password_hash(newpassword), email))
        connection.commit()

    # redirect to login page
    return redirect("/login")



# TODO: Code Result page
@app.route("/results")
@login_required
def results():    
    print("ID: "+ str(session["user_id"]))
    top10 = db.execute("SELECT celeb_id, user_id, name, MBTI, enne, points FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = ? ORDER BY points DESC LIMIT 10", (session["user_id"],))

    shortlist = []
    for row in top10:
        shortlist.append(row)
        print(row)
        
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