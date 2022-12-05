# Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Profiler guesses your age, gender and nationality


import json
import os

import pip._vendor.requests 

import sqlite3
from sqlite3 import Error


# def create_connection(path):
#     connection = None
#     try:
#         connection = sqlite3.connect("os.path.basename(celebs.db)")
#         # elif path == "E:\\users.db":
#         #     connection = sqlite3.connect("os.path.basename(users.db)")
#         #connection = sqlite3.connect("/Users/pzhang/Desktop/CS_Final_Project/CelebritiesAndPersonalities/celebs.db")
#         #connection2 = sqlite3.connect("os.path.basename(users.db)")
#         print("Connection to SQLite DB successful")
#     except Error as e:
#         print("The error occurred")

#     return connection

# connection = create_connection("E:\\celebs.db")


connection = sqlite3.connect("database.db")
# connection2 = sqlite3.connect("users.db")
# connection2 = create_connection("E:\\users.db")

db = connection.cursor()
# db2 = connection2.cursor()
# db2 = connection2.cursor()

# db.execute("DROP TABLE celebs")
# db.execute("CREATE TABLE if not exists celebs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, MBTI TEXT NOT NULL, enne TEXT NOT NULL, points NUMERIC)")

# db2.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)")

# celebs = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')
# characters = pip._vendor.requests.get('https://api.personality-database.com/api/v1/profiles?offset=0&limit=100000&pid=1&sort=top&property_id=1')

# celeb_data = (celebs.json()["profiles"])
# character_data = (characters.json()["profiles"])

# data = celeb_data + character_data
# #print(data)

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
    
    
# for person in data:
#     person_name = person["mbti_profile"]
#     person_personality = person["personality_type"]
#     mbti = person_personality.split()[0]
#     enne = person_personality.split()[1]
#     #print(person_name,mbti,enne)
    
    
#     db.execute("INSERT INTO celebs (name, MBTI, enne, points) VALUES (?, ?, ?, ?)", (person_name, mbti, enne, '0'))
#     connection.commit()

mbti = "ENTJ"
enne = 8
name = "Jack"
        
        # declaring each user's ratings as variables
mbti_rating = 1
enne_rating = 10
name_rating = 1
    
    # User initial api information
nationality = pip._vendor.requests.get('https://api.nationalize.io/?name='+name)
gender = pip._vendor.requests.get('https://api.genderize.io/?name='+name)
age = pip._vendor.requests.get('https://api.agify.io/?name='+name)

    # user-specific ai-generated nationality, gender, and age
user_nat = nationality.json()['country'][0]['country_id']
user_gen = gender.json()['gender']
user_age = age.json()['age']
    

print(user_nat)
print(user_gen)
print(user_age)

# for i in range(1, 10):
#     points = 0
#     mbti_points = 0
#     enne_points = 0
#     name_points = 0
    
#     celeb_mbti = db.execute("SELECT MBTI FROM celebs WHERE id = ?", (i,)).fetchone()[0]
#     celeb_full_name = db.execute("SELECT name FROM celebs WHERE id = ?", (i,)).fetchone()[0]
#     celeb_enne = db.execute("SELECT enne FROM celebs WHERE id = ?", (i,)).fetchone()[0]
#     celeb_name = celeb_full_name.split()[0]

    
#     for i in range(0, 4):
#         if celeb_mbti[i] == mbti[i]:
#             mbti_points += (0.25 * mbti_rating )
            
#     if int(celeb_enne[0]) == enne:
#         enne_points += enne_rating
        

#     name_exists = True
    
#     celeb_gender_search = pip._vendor.requests.get('https://api.genderize.io/?name='+celeb_name)
#     celeb_age_search = pip._vendor.requests.get('https://api.agify.io/?name='+celeb_name)
    
#     if celeb_gender_search.json()['count'] == 0:
#         name_exists = False
    
#     if name_exists:
#         celeb_nationality_search = pip._vendor.requests.get('https://api.nationalize.io/?name='+celeb_name)
#         celeb_nat = (celeb_nationality_search.json()['country'][0])['country_id']
#         celeb_gen = celeb_gender_search.json()['gender']
#         celeb_age = celeb_age_search.json()['age']
        
        
#         if celeb_nat == user_nat:
#             name_points += 1/3 * name_rating
        
#         if celeb_gen == user_gen:
#             name_points += 1/3 * name_rating
            
#         if celeb_age < (user_age + 5) and celeb_age > (user_age - 5):
#             name_points += 1/3 * name_rating


for i in range(1, 10):
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

    celeb_gender_search = pip._vendor.requests.get('https://api.genderize.io/?name='+celeb_name)
    celeb_age_search = pip._vendor.requests.get('https://api.agify.io/?name='+celeb_name)
    
    if celeb_gender_search.json()['count'] == 0:
        name_exists = False
    
    if name_exists:
        celeb_nationality_search = pip._vendor.requests.get('https://api.nationalize.io/?name='+celeb_name)
        celeb_nat = (celeb_nationality_search.json()['country'][0])['country_id']
        celeb_gen = celeb_gender_search.json()['gender']
        celeb_age = celeb_age_search.json()['age']
        
        
        if celeb_nat == user_nat:
            points += 1/3 * name_rating
        
        if celeb_gen == user_gen:
            points += 1/3 * name_rating
            
        if celeb_age < (user_age + 5) and celeb_age > (user_age - 5):
            points += 1/3 * name_rating
            
    print(i, celeb_name, celeb_nat, celeb_gen, celeb_age, celeb_mbti, celeb_enne, points)
    
    
    #output doesn't look correct - autoincremeent is off
    db.execute("INSERT INTO points (celeb_id, user_id, points) VALUES (?, ?, ?)", (i, 24, points))
    connection.commit()
    
    # db.execute("UPDATE celebs SET points = ? WHERE id = ?", (points, i))
    # connection.commit()
    
    
#SELECT * FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = 24 ORDER BY points DESC LIMIT 5;

#SELECT * FROM celebs WHERE id IN(SELECT celeb_id FROM points WHERE user_id = 24 ORDER BY points DESC LIMIT 5)
                                 
                                 
top20 = db.execute("SELECT celeb_id, user_id, name, MBTI, enne, points FROM points JOIN celebs ON points.celeb_id = celebs.id WHERE user_id = ? ORDER BY points DESC LIMIT 20", (24,))

for person in top20:
    print(person[0])

          
    

  
    

    # db.execute("UPDATE celebs SET points = ? WHERE id = ?", (points, i))
    #     #db.execute("INSERT INTO celebs(points) VALUES(?) WHERE id = ?", points, i)





db.close()



    

