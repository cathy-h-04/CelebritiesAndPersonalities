
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

# establishing database connection
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

# Index (home page of site)
@app.route("/")
def index():
    # Rendering our home page
    return render_template("index.html")

# About (displaying page about site's creators)
@app.route("/about", methods=["GET"])
def about():
        # Rendering about page
        return render_template("about.html")

# Methodology (displaying page showing our site's methodology)
@app.route("/methodology", methods=["GET"])
def methodology():
        # Rendering methodology page
        return render_template("methodology.html")
    

# Forgot password (for if users forgot password and need to set new one)
@app.route("/forgotpass", methods=["GET", "POST"])
def forgotpass():
    """Forgot password"""
    # rendering forgotpassword page if get method
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

        # make sure user inputs an email, password, confirmation, and security answers
        if not email:
            return apology("Must provide email.")

        elif not newpass:
            return apology("Must provide a new password.")

        elif not confirmpass:
            return apology("Must confirm new password.")

        elif not securityques1:
            return apology("Must answer both security questions.")

        elif not securityques2:
            return apology("Must answer both secuirty questions.")

        # Checking that the password has at least one digit, 1 special character, and 5 letters in their password
        # Declaring inital counter variables to zero
        digits = 0
        letters = 0
        special_characters = 0

        # Iterating through characters of password counting each type of character
        for char in newpass:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            else:
                special_characters += 1
                
        # Rendering error message if password does not meet specifications
        if letters < 5 or digits < 1 or special_characters < 1:
            return apology("New password must contain at least 5 letters, 1 digit, and 1 special character.")

          # 2nd personal touch, checks that password does not contain email
        elif newpass.find(email) != -1:
            return apology("Password must not contain email")

        # Check if old password equals new password
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        
        # Checking to see whether the inputted email exists within the database
        if rows is None:
           return apology("invalid email address", 403)

        # Ensuring the new password is not the same as the previous one
        if check_password_hash(rows[2], newpass):
            return apology("Repeated password", 403)

        # Checking that user correctly inputted security question 1
        if rows[3] != securityques1:
           return apology("The answer to one or more security questions is incorrect", 403)
 
        # Checking that user correctly inputted security question 2
        if rows[4] != securityques2:
           return apology("The answer to one or more security questions is incorrect", 403)

        # Update new password in database
        db.execute("UPDATE users SET password = ? WHERE email = ?", (generate_password_hash(newpass), email))
        connection.commit()

    # Redirect to login page
    return redirect("/login")


# Login (for allowing users to login)
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get user input
        email = request.form.get("email")
        password = request.form.get("password")

        # Get all information for that user inputted using their inputted email name
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        
        if len(rows) == 0 or not check_password_hash(rows[0][2], password):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout (for logging out users from site)
@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form since they've logged out
    return redirect("/")
    
    
# Test (for the celebrity matching test)
@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
     
    if request.method == "POST":        
    
        # Declaring user's input as variables
        mbti = request.form.get("MBTIs")
        enne = int(request.form.get("ENNEs")[0])
        name = request.form.get("firstname")
        
        # Declaring user's ratings as variables
        mbti_rating = int(request.form.get("mbtioptions"))
        enne_rating = int(request.form.get("enneoptions"))
        name_rating = int(request.form.get("nameoptions"))
        
        # User initial api information from genderize API
        gender = requests.get('https://api.genderize.io/?name='+name)
        age = requests.get('https://api.agify.io/?name='+name)

        # Setting name_exists (in our api's database) initially to true
        name_exists = True
        
        # Changing name_exists to false if name is not found in genderize API
            # Note: Agify, genderize, and nationalize APIs used here all share the same database of names
        if gender.json()['count'] == 0:
            name_exists = False
        
        # If name exists in database, finding nationality and determining most likley nationality, gender, and age based on inputted name
        if name_exists:
            # Nationality included here because, unlike gender and age APIs, will not run if name does not exist
            nationality = requests.get('https://api.nationalize.io/?name='+name)
            user_nat = (nationality.json()['country'][0])['country_id']
            user_gen = gender.json()['gender']
            user_age = int(age.json()['age'])

        # Fetching information for user in users database given their id
        rows = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchall()

        #  Deleting previous results for user
        if len(rows) != 0:
            db.execute("DELETE FROM points WHERE id = ?", (session["user_id"],))

        #  Iterating through all celebrities in our celebs database
        for i in range(1, CELEB_COUNT + 1):
            # Setting points counter variable for each celeb to zero
            points = 0
        
            # Selecting appropriate information for each celebrity
            celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_nat = db.execute("SELECT nationality FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_gen = db.execute("SELECT gender FROM celebs WHERE id = ?", (i,)).fetchone()[0]
            celeb_age = db.execute("SELECT age FROM celebs WHERE id = ?", (i,)).fetchone()[0]
    
            #  If the (agify-generated beforehand) age for celebrity is not None/N/A (meaning age exists)
            if celeb_age != "N/A" and celeb_age is not None:
                # Casting celeb_age as int for next if
                celeb_age = int(celeb_age)
                # If agify-generated celeb_age is within 10 years of agify-generated user_age
                if celeb_age < (user_age + 5) and celeb_age > (user_age - 5):
                    # Add 1/3 worth of name rating
                    points += 1/3 * name_rating

            # 
            for j in range(0, 4):
                if celeb_mbti[j] == mbti[j]:
                    points += (0.25 * mbti_rating )
                    
            if int(celeb_enne[0]) == enne:
                points += enne_rating
                
            if celeb_nat == user_nat:
                points += 1/3 * name_rating
            
            if celeb_gen == user_gen:
                points += 1/3 * name_rating
                
            db.execute("INSERT INTO points (celeb_id, user_id, points) VALUES (?, ?, ?)", (i, session["user_id"], points))
        connection.commit()

            
        return redirect("/results")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("test.html")
    
# Register (user registration)
@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()
    
    # Rendering register again if get method
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # Creating variables all of the user-inputted information when registering
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmpassword")
        securityques1 = request.form.get("securityques1")
        securityques2 = request.form.get("securityques2")

        # Ensure password was submitted
        if not password:
            return apology("Must provide password", 400)

        # Ensure email was submitted
        elif not email:
            return apology("Must provide email", 400)

        # Checking that user has confirmed password
        elif not confirmation:
            return apology("Must confirm password", 400)
        
        # Checking that user answered first security question
        elif not securityques1:
            return apology("Must input the answer to first security question.")

        # Checking that user answered second security question
        elif not securityques2:
            return apology("Must input the answer to second security question.")

        # Checking that email and password match
        elif password != confirmation:
            return apology("password and confirmation password must match", 400)


        # Checking that the password has at least one digit, 1 special character, and 5 letters in their password
        # Creating counter variables for each component of password
        digits = 0
        letters = 0
        special_characters = 0

        # Iterating through the letters of the password to check each component's count
        for char in password:
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
            else:
                special_characters += 1

        # Returning apology if password does not match specifications
        if letters < 5 or digits < 1 or special_characters < 1:
            return apology("Password must contain at least 5 letters, 1 digit, and 1 special character.")

        # Ensuring that password does not contain the email (otherwise could make easier to guess password)
        elif password.find(email) != -1:
            return apology("Password must not contain email")
        
        # Checking that email is unique for the account
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        print("FIRST CHECK")
        if len(rows) > 0:
            return apology("email already exists", 400)

        # Adding user's email and hashed password into database
        db.execute("INSERT INTO users (email, password, maiden, nickname) VALUES(?, ?, ?, ?)", (email, generate_password_hash(password), securityques1, securityques2))
        connection.commit()

        # Confirm registration
        return redirect("/login")


# Change password (for users changing password))
@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():

    if request.method == "GET":
        # Rendering changepass page if GET is used
        return render_template("changepass.html")

    # user reached route via POST
    else:

        # Creating variables for user-inputted info
        email = request.form.get("email")
        oldpassword = request.form.get("old_password")
        newpassword = request.form.get("new_password")
        newconfirmation = request.form.get("new_confirmation")

        # Ensuring all fields have been completed
        if not email:
            return apology("Must provide email.")

        elif not oldpassword:
            return apology("Must provide the old password.")

        elif not newpassword:
            return apology("Must input new password.")

        elif not newconfirmation:
            return apology("Must input confirm new password.")

        # Finding user information entered given the inputted email
        rows = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        
        # Checking to see whether the inputted email exists within the database
        if rows is None:
           return apology("invalid email address", 403)
       
         # Check to see if new password has been repeated
        if check_password_hash(rows[2], newpassword):
            return apology("Repeated password", 403)
    
        # Ensuring that old password matches the account specified
        if len(rows) == 0 or not check_password_hash(rows[2], oldpassword):
            return apology("invalid email and/or password", 403)

        # 2nd personal touch, checks that password does not contain email
        if newpassword.find(email) != -1:
            return apology("Password must not contain email")
        
        # Returning apology if old password is same as the new one
        if oldpassword != newconfirmation:
           return apology("password and confirmation password must match", 400)

        # Update new password into database
        db.execute("UPDATE users SET password = ? WHERE email = ?", (generate_password_hash(newpassword), email))
        connection.commit()

    # Redirect to login page
    return redirect("/login")


# Results (for displaying top 10 celebrity matches)
@app.route("/results")
@login_required
def results():  
    # Retrieving celebrities with highest points count for given user and their input  
    top10 = db.execute("SELECT DISTINCT user_id, name, MBTI, enne, points FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = ? ORDER BY points DESC LIMIT 10", (session["user_id"],))

    # Creating list for celebrities
    shortlist = []
    
    # Populating shortlist with 10 highest scoring celebrities
    for row in top10:
        shortlist.append(row)
        
    # Returning results page and passing in the shortlist of celebrity matches    
    return render_template("results.html", shortlist = shortlist)
