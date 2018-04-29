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
		self.full_name = ""
		self.title = ""
		self.company = ""
		self.linked_in = ""



	def __eq__(self, other):
		return int(self.id) == int(other.id)


	def addToDatabase(self):
		with sql.connect('database.db') as connection:
			cursor1 = connection.cursor()
			cursor1.execute("INSERT INTO users (username, email, password_hash, full_name, title, company, linked_in, interests) VALUES (?,?,?,?,?,?,?,?)",(self.username, self.email, self.password_hash, "", "", "", "", "[]"))
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

	def getContacts(self):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			result = cursor.execute("SELECT user2 FROM contacts WHERE user1 = ?", (self.id)).fetchall()
			lst_contacts = []
			for entry in result:
				lst_contacts.append((getUserByID(entry[0])))
			return lst_contacts


	def updateInfoFullname(self, fullname):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE users SET full_name = ? WHERE user_id = ?;",(fullname, self.id))
			connection.commit()

	def updateInfoTitle(self, title):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE users SET title = ? WHERE user_id = ?;",(title, self.id))
			connection.commit()

	def updateInfoCompany(self, company):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE users SET company = ? WHERE user_id = ?;",(company, self.id))
			connection.commit()

	def updateInfolinkedin(self, linkedin):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE users SET linked_in = ? WHERE user_id = ?;",(linkedin, self.id))
			connection.commit()


	def getProfInfo(self):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			result = cursor.execute("SELECT full_name, title, company, linked_in FROM users WHERE user_id = ?", (self.id,)).fetchall()
			full_name = result[0][0]
			title = result[0][1]
			company = result[0][2]
			linked_in = result[0][3]
		return full_name, title, company, linked_in

	def getInterests(self):
		with sql.connect('database.db') as connection:
			cursor = connection.cursor()
			result = cursor.execute("SELECT interests FROM users WHERE user_id = ?", (self.id,)).fetchall()
			return result[0][0]





def findCommonInterests(user1_id, user2_id):
	with sql.connect('database.db') as connection:
		cursor1 = connection.cursor()
		result1 = cursor1.execute("SELECT interests FROM users WHERE user_id = ?", (user1_id,)).fetchall()
		result1 = json.loads(result1[0][0])
		cursor2 = connection.cursor()
		result2 = cursor2.execute("SELECT interests FROM users WHERE user_id = ?", (user2_id,)).fetchall()
		result2 = json.loads(result2[0][0])
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


def getNumUsers():
	with sql.connect('database.db') as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT COUNT (*) FROM users;").fetchall()
	return result[0][0]





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
		full_name, title, company, linked_in = user.getProfInfo()
		user.fullname = full_name
		user.title = title
		user.company = company
		user.linkedin = linked_in	
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
		full_name, title, company, linked_in = user.getProfInfo()
		user.fullname = full_name
		user.title = title
		user.company = company
		user.linkedin = linked_in	
		return user


""" When new value is added to subscribed to feed 
"""
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	print("hello")

		
@login_manager.user_loader
def load_user(id):
	return getUserByID(id)


	
