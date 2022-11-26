# Cathy Hou Anh-Thu Le YAY 
# Personal touch: requires password have at least 5 letters, 1 number, and 1 special character

#heello my name is Jeff
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

"this is where I addeed new code"

# what is going on skdfhsodfha

@app.route("/")
@login_required
def index():
    # query for the sum of shares for a symbol and the symbol across all of the user's transactions
    stock_data = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    # keeping track of a variable for the total value of all of the user's stocks
    stock_total = 0

    # looping through all of a user's transactions
    for row in stock_data:

        # looking up symbol to get a dictionary wth current name, price, symbol of stock
        item = lookup(row["symbol"])

        # calculating the total price for the row
        total = item["price"] * row["shares"]

        # adding a field total and corresponding value for the row
        row["total"] = total

        # updating total value of all the user's stocks
        stock_total += total

        # adding a field name and finding name value of the stock
        row["name"] = item["name"]

        # adding a field price and finding price value of the stock
        row["price"] = item["price"]

    # query to find the user's cash as key value pair
    user_balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # finding the actual cash value
    cash = user_balance[0]["cash"]

    grand_total = stock_total + cash

    return render_template("index.html", stock_data=stock_data, grand_total=grand_total, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        # looking up the symbol from user input, getting a dictionary describing the stock in return
        stock = lookup(request.form.get("symbol"))
        symbol = request.form.get("symbol")

        # finding the user's current cash amount
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # checking that user has inputted a symbol
        if not symbol:
            return apology("must provide symbol", 403)

        # checking that symbol exists
        elif not stock:
            return apology("symbol does not exist", 400)

        # checking that user has inputted number of shares they want
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        # checking that shares is a positive integer
        elif not (request.form.get("shares").isdigit() and int(request.form.get("shares")) > 0):
            return apology("shares must be a positive integer", 400)

        shares = int(request.form.get("shares"))

        # checking that stock price does not exceed user cash balance
        if stock["price"] * shares > balance[0]["cash"]:
            return apology("Insufficient balance to purchase stock", 403)

        # assigning variables using dictionary of stock with user's symbol
        currentPrice = stock["price"]
        name = stock["name"]
        # just in case lookup still runs but the symbol is slightly mispelled
        symbol = stock["symbol"]

        total = shares * currentPrice
        timestamp = datetime.now()

        # inserting row into transactions representing this purchase
        db.execute("INSERT INTO transactions (user_id, shares, symbol, price, name, total, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], shares, symbol, currentPrice, name, total, timestamp)

        # updating user's price after buying stock
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total, session["user_id"])

        # redirects them back to the portfolio after submitting
        return redirect("/")

    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # querying for all of the user's transactions
    user_transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=user_transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":

        # checking that user has inputted a symbol
        if not request.form.get("symbol"):
            return apology("must input a symbol")

        # looking up stock for user's symbol
        stock = lookup(request.form.get("symbol"))

        # checking that symbol exists
        if not stock:
            return apology("symbol doesn't exist")
        else:
            return render_template("quoted.html", stock=stock)

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
        confirmation = request.form.get("confirmation")

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

        # personal touch: checking that the password has at least one digit, 1 special character, and 5 letters in their password
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    # querying for all of the symbols corresponding to the stocks of the user for which there is at least 1 share
    symbols = db.execute(
        "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    if request.method == "POST":

        symbol_input = request.form.get("symbol")

        # finding the user's total shares of the stock corresponding to the inputted symbol
        stock_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                  session["user_id"], request.form.get("symbol"))[0]["shares"]

        # checking that symbol has been inputted
        if not symbol_input:
            return apology("must select symbol", 400)

        # checking that shares has been inputted
        elif not request.form.get("shares"):
            return apology("must input number of shares", 400)

        # checking that shares is a positive integer
        elif not (request.form.get("shares").isdigit() and int(request.form.get("shares")) > 0):
            return apology("shares must be a positive integer", 400)

        # checking that user has enough shares of stock that they want to sell
        elif int(request.form.get("shares")) > stock_shares:
            return apology("not enough shares of stock", 400)

        adjust_shares = int(request.form.get("shares"))

        stock = lookup(symbol_input)
        currentPrice = stock["price"]
        symbol = stock["symbol"]
        name = stock["name"]
        total = currentPrice * adjust_shares
        timestamp = datetime.now()

        # inputting user's sale into transactions database
        db.execute("INSERT INTO transactions (user_id, shares, symbol, price, name, total, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], adjust_shares * -1, symbol, currentPrice, name, total, timestamp)

    # updating user's cash value
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", symbols=symbols)


# Cathy Hou
# Personal touch: requires password have at least 5 letters, 1 number, and 1 special character

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # query for the sum of shares for a symbol and the symbol across all of the user's transactions
    stock_data = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])

    # keeping track of a variable for the total value of all of the user's stocks
    stock_total = 0

    # looping through all of a user's transactions
    for row in stock_data:

        # looking up symbol to get a dictionary wth current name, price, symbol of stock
        item = lookup(row["symbol"])

        # calculating the total price for the row
        total = item["price"] * row["shares"]

        # adding a field total and corresponding value for the row
        row["total"] = total

        # updating total value of all the user's stocks
        stock_total += total

        # adding a field name and finding name value of the stock
        row["name"] = item["name"]

        # adding a field price and finding price value of the stock
        row["price"] = item["price"]

    # query to find the user's cash as key value pair
    user_balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # finding the actual cash value
    cash = user_balance[0]["cash"]

    grand_total = stock_total + cash

    return render_template("index.html", stock_data=stock_data, grand_total=grand_total, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        # looking up the symbol from user input, getting a dictionary describing the stock in return
        stock = lookup(request.form.get("symbol"))
        symbol = request.form.get("symbol")

        # finding the user's current cash amount
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # checking that user has inputted a symbol
        if not symbol:
            return apology("must provide symbol", 403)

        # checking that symbol exists
        elif not stock:
            return apology("symbol does not exist", 400)

        # checking that user has inputted number of shares they want
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        # checking that shares is a positive integer
        elif not (request.form.get("shares").isdigit() and int(request.form.get("shares")) > 0):
            return apology("shares must be a positive integer", 400)

        shares = int(request.form.get("shares"))

        # checking that stock price does not exceed user cash balance
        if stock["price"] * shares > balance[0]["cash"]:
            return apology("Insufficient balance to purchase stock", 403)

        # assigning variables using dictionary of stock with user's symbol
        currentPrice = stock["price"]
        name = stock["name"]
        # just in case lookup still runs but the symbol is slightly mispelled
        symbol = stock["symbol"]

        total = shares * currentPrice
        timestamp = datetime.now()

        # inserting row into transactions representing this purchase
        db.execute("INSERT INTO transactions (user_id, shares, symbol, price, name, total, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], shares, symbol, currentPrice, name, total, timestamp)

        # updating user's price after buying stock
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total, session["user_id"])

        # redirects them back to the portfolio after submitting
        return redirect("/")

    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # querying for all of the user's transactions
    user_transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=user_transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":

        # checking that user has inputted a symbol
        if not request.form.get("symbol"):
            return apology("must input a symbol")

        # looking up stock for user's symbol
        stock = lookup(request.form.get("symbol"))

        # checking that symbol exists
        if not stock:
            return apology("symbol doesn't exist")
        else:
            return render_template("quoted.html", stock=stock)

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
        confirmation = request.form.get("confirmation")

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

        # personal touch: checking that the password has at least one digit, 1 special character, and 5 letters in their password
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    # querying for all of the symbols corresponding to the stocks of the user for which there is at least 1 share
    symbols = db.execute(
        "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    if request.method == "POST":

        symbol_input = request.form.get("symbol")

        # finding the user's total shares of the stock corresponding to the inputted symbol
        stock_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                  session["user_id"], request.form.get("symbol"))[0]["shares"]

        # checking that symbol has been inputted
        if not symbol_input:
            return apology("must select symbol", 400)

        # checking that shares has been inputted
        elif not request.form.get("shares"):
            return apology("must input number of shares", 400)

        # checking that shares is a positive integer
        elif not (request.form.get("shares").isdigit() and int(request.form.get("shares")) > 0):
            return apology("shares must be a positive integer", 400)

        # checking that user has enough shares of stock that they want to sell
        elif int(request.form.get("shares")) > stock_shares:
            return apology("not enough shares of stock", 400)

        adjust_shares = int(request.form.get("shares"))

        stock = lookup(symbol_input)
        currentPrice = stock["price"]
        symbol = stock["symbol"]
        name = stock["name"]
        total = currentPrice * adjust_shares
        timestamp = datetime.now()

        # inputting user's sale into transactions database
        db.execute("INSERT INTO transactions (user_id, shares, symbol, price, name, total, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], adjust_shares * -1, symbol, currentPrice, name, total, timestamp)

    # updating user's cash value
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", symbols=symbols)


