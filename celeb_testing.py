# Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Profiler guesses your age, gender and nationality


import json
import os

import pip._vendor.requests 

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect("os.path.basename(celebs.db)")
        # elif path == "E:\\users.db":
        #     connection = sqlite3.connect("os.path.basename(users.db)")
        #connection = sqlite3.connect("/Users/pzhang/Desktop/CS_Final_Project/CelebritiesAndPersonalities/celebs.db")
        #connection2 = sqlite3.connect("os.path.basename(users.db)")
        print("Connection to SQLite DB successful")
    except Error as e:
        print("The error occurred")

    return connection

connection = create_connection("E:\\celebs.db")
connection2 = sqlite3.connect("users.db")
# connection2 = create_connection("E:\\users.db")

db = connection.cursor()
db2 = connection2.cursor()
# db2 = connection2.cursor()

db.execute("DROP TABLE celebs")
db.execute("CREATE TABLE if not exists celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")

db2.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)")

celebs = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
characters = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])
character_data = (characters.json()["profiles"])

data = celeb_data + character_data
#print(data)

#print(len(data))

# for i in range(100):
# for celeb in celeb_data:
#     celeb_personality = celeb["personality_type"]
#     mbti = celeb_personality.split()[0]
#     enne = celeb_personality.split()[1]
#     print(celeb_name,mbti,enne)
#     db.execute("INSERT INTO celebs (name, MBTI, enne, points) VALUES (?, ?, ?, ?)", (celeb_name, mbti, enne, '0'))
    
#     connection.commit()


    
    #print(celeb_name, celeb_personality)
    
    
for person in data:
    person_name = person["mbti_profile"]
    person_personality = person["personality_type"]
    mbti = person_personality.split()[0]
    enne = person_personality.split()[1]
    #print(person_name,mbti,enne)
    
    
    db.execute("INSERT INTO celebs (name, MBTI, enne, points) VALUES (?, ?, ?, ?)", (person_name, mbti, enne, '0'))
    connection.commit()
    
db.execute("SELECT * FROM celebs")

db.close()
db2.close()



    

