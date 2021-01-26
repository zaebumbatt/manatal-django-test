import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


client = MongoClient(os.getenv('MC'))
db = client['logs_mongodb']

users = db['users']
schools = db['schools']
students = db['students']
