import os
import pymongo

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class Repository:
	# initialize db
	def __init__(self):

		db_username = os.getenv("DB_USERNAME")
		db_password = os.getenv("DB_PASSWORD")

		db_url = "mongodb+srv://{}:{}@deaglewatch.trylq.mongodb.net/DeagleWatch?retryWrites=true&w=majority".format(db_username, db_password)

		db_client = pymongo.MongoClient(db_url)

		db_cluster = db_client["DeagleWatch"]
		self.collection = db_cluster["DeagleWatch"]

	# persists a single steam account to db	
	def saveOne(self, steam_id):
		query = {"steam_id": steam_id}

		if self.findOne(steam_id) == None:
			account = self.collection.insert_one(query)
			return "Account added"
		else:
			return "Account already on watch"
        

    # finds entry in db with given url
	def findOne(self, steam_id):
		query = {"steam_id": steam_id}
		account = self.collection.find_one(query)
		return account

	def removeOne(self, steam_id):
		query = {"steam_id": steam_id}
		account = self.collection.delete_one(query)
		return f"Account removed"





