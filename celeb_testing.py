# Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Profiler guesses your age, gender and nationality
import requests
import json

# User's input
# user_name = input("Input your first name: ")

# Nationality
celebs = requests.get('https://api.personality-database.com/api/v1/profiles?offset=1&limit=100&pid=1&sort=top&property_id=1')
# gender = requests.get('https://api.genderize.io/?name='+user_name)
# age = requests.get('https://api.agify.io/?name='+user_name)

celeb_data = (celebs.json()["profiles"])
# age_data = gender.json()['gender']
# gen_data = age.json()['age']

celeb_name = celeb_data[0]["mbti_profile"]

# print(new_data)
# print('gender: ', age_data)
# print('age: ', gen_data)

for i in range(100):
    celeb_name = celeb_data[i]["mbti_profile"]
    celeb_personality = celeb_data[i]["personality_type"]
    
    print(celeb_name, celeb_personality)
    

