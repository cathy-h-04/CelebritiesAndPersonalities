# FIRST CHECK:
    
#     TYPE: 
#     sqlite3 database.db
#     .schema
    
#     Should see:

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


#EXECUTE THIS ONCE AT THE VERY BEGGINNING. 

connection = sqlite3.connect("database.db", check_same_thread=False)

db = connection.cursor()

db.execute("DELETE FROM points")
db.execute("DELETE FROM sqlite_sequence where name='points'")


db.execute("DELETE FROM users")
db.execute("DELETE FROM sqlite_sequence where name='users'")



db.execute("DELETE FROM celebs")
db.execute("DELETE FROM sqlite_sequence where name='celebs'")


celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
characters = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])
character_data = (characters.json()["profiles"])

data = celeb_data + character_data


for person in data:
    person_name = person["mbti_profile"]
    person_personality = person["personality_type"]
    mbti = person_personality.split()[0]
    enne = person_personality.split()[1]
    #print(person_name,mbti,enne)

    db.execute("INSERT INTO celebs (name, MBTI, enne) VALUES (?, ?, ?)", (person_name, mbti, enne))
    connection.commit()
    
    
# CHECK AND SEE IF THIS SUCESFULLY INPUTS INTO DATABASE! SHOULD HAVE 600 ROWS



#MIGHT HAVE SOMEE ISSUES WITH THE THREAD. I BASICALLY COMMITED A NEW CONNECTION HERE BC ITS A DIFF FILE FROM APP.PY. IF THAT DOESNT WORK, TRY USING THE SAME CONNECTION BELLOW: 
# connection = sqlite3.connect("database.db", check_same_thread=False)
# db = connection.cursor()

