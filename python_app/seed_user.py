import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB = os.getenv("MONGODB_DB", "tododb")

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
users = db["users"]

username = "admin"
password = "admin123"

existing = users.find_one({"username": username})
if existing:
    print(f"User '{username}' already exists.")
else:
    users.insert_one({"username": username, "password": password})
    print(f"Created user '{username}' with password '{password}'.")
