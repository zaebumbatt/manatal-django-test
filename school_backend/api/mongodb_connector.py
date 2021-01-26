import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


client = MongoClient(os.getenv('MC'))
db = client["logs_mongodb"]

col = db["actions"]
print(os.getenv('MC'))