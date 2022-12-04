import sqlite3
from sqlite3 import Error
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required


connection = sqlite3.connect("database.db")
db = connection.cursor()

email = "hi"
password = "hello"
securityques1 = "le"
securityques2 = "fam"


db.execute("INSERT INTO users (email, password, maiden, nickname) VALUES(?, ?, ?, ?)", (email, generate_password_hash(password), securityques1, securityques2))
connection.commit()