import csv
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_username = os.getenv("MONGODB_ACCOUNT")
mongo_password = os.getenv("MONGODB_ACCOUNT_PASS")

MONGO_URI = f"mongodb+srv://adityaramesh15:{mongo_password}@cs498-hw3.s3qfsxq.mongodb.net/?appName=CS498-HW3"
client = MongoClient(MONGO_URI)

db = client['ev_db']
collection = db['vehicles']


csv_file_path = 'Electric_Vehicle_Population_Data.csv'
batch_size = 5000
batch = []

with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        batch.append(row)

        if len(batch) == batch_size:
            collection.insert_many(batch)
            batch = []
    
    if batch:
        collection.insert_many(batch)
        batch = []
