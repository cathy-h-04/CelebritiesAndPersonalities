import os

import sqlite3
from sqlite3 import Error

import json

from pip._vendor import requests

#from flask_session import Session
#from tempfile import mkdtemp
#app = Flask(__name__)

import sqlite3
from sqlite3 import Error


# FIRST CHECK:
    
#     TYPE: 
#     sqlite3 database.db
#     .schema
    
#     Should see:



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


# CREATE TABLE celebs (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#                 name TEXT NOT NULL, 
#                 MBTI TEXT NOT NULL, 
#                 enne TEXT NOT NULL,
#                 nationality TEXT,
#                 gender TEXT,
#                 age NUMBER
#             );


#EXECUTE THIS ONCE AT THE VERY BEGGINNING. 

connection = sqlite3.connect("database.db", check_same_thread=False)

db = connection.cursor()

# db.execute("DELETE FROM points")
# db.execute("DELETE FROM sqlite_sequence where name='points'")


# db.execute("DELETE FROM users")
# db.execute("DELETE FROM sqlite_sequence where name='users'")



celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
characters = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])
character_data = (characters.json()["profiles"])

data = celeb_data + character_data

#for person in data:

for person in data:
    
    name_exists = True
    
    person_full_name = person["mbti_profile"]
    person_name = person_full_name.split()[0]
    person_personality = person["personality_type"]
    mbti = person_personality.split()[0]
    enne = person_personality.split()[1]
    
    person_nat = "N/A"
    person_gen = "N/A"
    person_age = "N/A"
    
    person_gender_search = requests.get('https://api.genderize.io/?name='+person_name)
    person_age_search = requests.get('https://api.agify.io/?name='+person_name)
    
    if person_gender_search.json()['count'] == 0:
        name_exists = False

    if name_exists:
        person_nationality_search = requests.get('https://api.nationalize.io/?name='+person_name)
        person_nat = (person_nationality_search.json()['country'][0])['country_id']
        person_gen = person_gender_search.json()['gender']
        person_age = person_age_search.json()['age']

    db.execute("INSERT INTO celebs (name, MBTI, enne, nationality, gender, age) VALUES (?, ?, ?, ?, ?, ?)", (person_full_name, mbti, enne, person_nat, person_gen, person_age))
    connection.commit()

    
    
# CHECK AND SEE IF THIS SUCESFULLY INPUTS INTO DATABASE! SHOULD HAVE 600 ROWS



#MIGHT HAVE SOMEE ISSUES WITH THE THREAD. I BASICALLY COMMITED A NEW CONNECTION HERE BC ITS A DIFF FILE FROM APP.PY. IF THAT DOESNT WORK, TRY USING THE SAME CONNECTION BELLOW: 
# connection = sqlite3.connect("database.db", check_same_thread=False)
# db = connection.cursor()

