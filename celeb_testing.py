# Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Profiler guesses your age, gender and nationality

import json
import os

import requests


#from flask import Flask, flash, redirect, render_template, request, session
#from flask_session import Session
#from tempfile import mkdtemp
#app = Flask(__name__)

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect("/Users/pzhang/Desktop/CS_Final_Project/CelebritiesAndPersonalities/celebs.db")
        print("Connection to SQLite DB successful")
    except Error as e:
        print("The error occurred")

    return connection

connection = create_connection("E:\\celebs.db")

db = connection.cursor()

#db.execute("CREATE TABLE celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")




# User's input
# user_name = input("Input your first name: ")

# Nationality

celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

celeb_data = (celebs.json()["profiles"])


print(len(celeb_data))

#for i in range(100):
for celeb in celeb_data:
    celeb_name = celeb["mbti_profile"]
    celeb_personality = celeb["personality_type"]
    mbti = celeb_personality.split()[0]
    enne = celeb_personality.split()[1]
    print(celeb_name,mbti,enne)
    db.execute("INSERT into celebs (name, MBTI, enne, points) VALUES (?, ?, ?, ?)", celeb_name, mbti, enne, '0')


    
    #print(celeb_name, celeb_personality)
    

