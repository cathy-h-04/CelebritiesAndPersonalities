
# #THIS IS HOW WE CREATED THE DATA

# import os

# import sqlite3
# from sqlite3 import Error

# # from cs50 import SQL
# from flask import Flask, flash, redirect, render_template, request, session

# from flask_session import Session
# # from flask_session import Session
# from tempfile import mkdtemp

# from werkzeug.security import check_password_hash, generate_password_hash
# from datetime import datetime

# # importing helper functions
# from helpers import apology, login_required

# import json

# from pip._vendor import requests
# #from tempfile import mkdtemp
# #app = Flask(__name__)

# import sqlite3
# from sqlite3 import Error


# # CREATE TABLE users (
# #                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
# #                 email TEXT NOT NULL, 
# #                 password TEXT NOT NULL, 
# #                 maiden TEXT NOT NULL, 
# #                 nickname TEXT NOT NULL
# #             );



# # CREATE TABLE points (
# #                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# #                 celeb_id INTEGER NOT NULL,
# #                 user_id INTEGER NOT NULL,
# #                 points NUMERIC,
# #                 FOREIGN KEY(celeb_id) REFERENCES celebs(id),
# #                 FOREIGN KEY(user_id) REFERENCES users(id)
# #             );


# # CREATE TABLE celebs (
# #                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
# #                 name TEXT NOT NULL, 
# #                 MBTI TEXT NOT NULL, 
# #                 enne TEXT NOT NULL,
# #                 nationality TEXT,
# #                 gender TEXT,
# #                 age NUMBER
# #             );


# connection = sqlite3.connect("database.db", check_same_thread=False)

# db = connection.cursor()



# # db.execute("DELETE FROM points")
# # db.execute("DELETE FROM sqlite_sequence where name='points'")


# # db.execute("DELETE FROM users")
# # db.execute("DELETE FROM sqlite_sequence where name='users'")


# #Accessed as much data as possible from the personality database

# celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

# data = (celebs.json()["profiles"])

# for person in data:
    
#     name_exists = True
    
#     person_full_name = person["mbti_profile"]
#     person_name = person_full_name.split()[0]
#     person_personality = person["personality_type"]
#     mbti = person_personality.split()[0]
#     enne = person_personality.split()[1]
    
#     person_nat = "N/A"
#     person_gen = "N/A"
#     person_age = "N/A"
    
#     person_gender_search = requests.get('https://api.genderize.io/?name='+person_name)
#     person_age_search = requests.get('https://api.agify.io/?name='+person_name)
    
#     if person_gender_search.json()['count'] == 0:
#         name_exists = False

#     if name_exists:
#         person_nationality_search = requests.get('https://api.nationalize.io/?name='+person_name)
#         person_nat = (person_nationality_search.json()['country'][0])['country_id']
#         person_gen = person_gender_search.json()['gender']
#         person_age = person_age_search.json()['age']

#     db.execute("INSERT INTO celebs (name, MBTI, enne, nationality, gender, age) VALUES (?, ?, ?, ?, ?, ?)", (person_full_name, mbti, enne, person_nat, person_gen, person_age))
#     connection.commit()

