from pip._vendor import requests

name = input("name: \n")

gender = requests.get('https://api.genderize.io/?name='+name)

print(gender)