# TODO: EDIT THIS! THIS IS COPIED FROM THE FINANCE PSET!


import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

import requests
import json



# TODO: alter apology to be specific to our website (if this is how we want to present edgecases)
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# TODO: cater to our code if desired (since copied from PSET)
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# TODO: this is where we will add our own special API Key (SCRAPING!)
def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def name_characteristics(name):
 # Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Takes the user's inputted name as the input
    nationality = requests.get('https://api.nationalize.io/?name='+name)
    gender = requests.get('https://api.genderize.io/?name='+name)
    age = requests.get('https://api.agify.io/?name='+name)

    nationality = (nationality.json()['country'][0])['country_id']
    gender = gender.json()['gender']
    age = age.json()['age']

    return age, gender, nationality
