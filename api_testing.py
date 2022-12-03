# Credit for the below code: https://forum.freecodecamp.org/t/extracting-data-from-json/452527
# Profiler guesses your age, gender and nationality
import requests
import json

# User's input
user_name = input("Input your first name: ")

# Nationality
nationality = requests.get('https://api.nationalize.io/?name='+user_name)
gender = requests.get('https://api.genderize.io/?name='+user_name)
age = requests.get('https://api.agify.io/?name='+user_name)

nat_data = (nationality.json()['country'][0])['country_id']
age_data = gender.json()['gender']
gen_data = age.json()['age']

print('nationality: ', nat_data)
print('gender: ', age_data)
print('age: ', gen_data)