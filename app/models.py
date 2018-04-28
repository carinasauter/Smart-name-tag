import sqlite3 as sql
from app import login_manager, db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import requests
import json
from app import login_manager, db, mqtt
from Adafruit_IO import MQTTClient


class User(UserMixin):

	def __init__(self, username, email, password_hash):
		self.id = 0;
		self.username = username
		self.email = email
		self.password_hash = password_hash


	def __eq__(self, other):
		return int(self.id) == int(other.id)


	def addToDatabase(self):
		with sql.connect('database.db') as connection:
			cursor1 = connection.cursor()
			cursor1.execute("INSERT INTO users (username, email, password_hash) VALUES (?,?,?)",(self.username, self.email, self.password_hash))
			cursor2 = connection.cursor()
			result = cursor2.execute("SELECT LAST_INSERT_ROWID()").fetchall()
			result = result[0][0]
			connection.commit()
			self.id = result

	def getId(self):
		return self.id

	def updateUserInterests(self, interests):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE users SET interests = ? WHERE user_id = ?;",(interests, self.id))
			connection.commit()

	def getContacts():
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			result = cursor.execute("SELECT user2 FROM contacts WHERE user1 = ?", (current_user.id)).fetchall()
			return result[0][0]


def findCommonInterests(user1_id, user2_id):
	with sql.connect('database.db') as connection:
		cursor1 = connection.cursor()
		result1 = cursor1.execute("SELECT interests FROM users WHERE user_id = ?", (user1_id,)).fetchall()
		print(result1[0][0])
		result1 = json.loads(result1[0][0])
		cursor2 = connection.cursor()
		result2 = cursor2.execute("SELECT interests FROM users WHERE user_id = ?", (user2_id,)).fetchall()
		result2 = json.loads(result2[0][0])
		print(type(result2))
	return intersection(result1, result2)


def addContact(user1_id, user2_id):
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO contacts (user1, user2) VALUES (?,?)",(user1_id, user2_id))
		connection.commit()



def intersection(lst1, lst2):
	lst3 = []
	for entry in lst1:
		if entry in lst2:
			lst3.append(entry)
	return lst3






	



""" Takes a username as parameter and checks in the database. If the user exists, 
returns user object. If not, returns None.
"""
def getUserByUsername(query):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (query,))
		result = cursor.fetchall()
		if len(result) == 0:
			return None
		else:
			row = result[0]
			user = User(query, row[2], row[3])
			user.id = row[0]
			return user


""" Takes a userID as parameter and checks in the database. If the user exists, 
returns user object. If not, returns None.
"""
def getUserByID(query):
	with sql.connect('database.db') as connection:
		connection.row_factory = sql.Row
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE user_id = (?)", (query,))
		result = cursor.fetchall()
		if len(result) == 0:
			return None
		else:
			row = result[0]
			user = User(row[1], row[2], row[3])
			user.id = query
			return user


""" When new value is added to subscribed to feed 
"""
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	print("hello")

		
@login_manager.user_loader
def load_user(id):
	return getUserByID(id)


	
