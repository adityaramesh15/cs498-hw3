from flask import Flask, request, jsonify
from pymongo import MongoClient, WriteConcern, ReadPreference
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
mongo_username = os.getenv("MONGODB_ACCOUNT")
mongo_password = os.getenv("MONGODB_ACCOUNT_PASS")

MONGO_URI = f"mongodb+srv://{mongo_username}:{mongo_password}@cs498-hw3.s3qfsxq.mongodb.net/?appName=CS498-HW3"
client = MongoClient(MONGO_URI)

db = client['ev_db']
base_collection = db['vehicles']


@app.route('/insert-fast', methods=['POST'])
def insert_fast():
    """1. Fast but Unsafe Write (Primary Only)"""
    data = request.json
    fast_collection = base_collection.with_options(write_concern=WriteConcern(w=1))
    
    result = fast_collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route('/insert-safe', methods=['POST'])
def insert_safe():
    """2. Highly Durable Write (Majority)"""
    data = request.json
    safe_collection = base_collection.with_options(write_concern=WriteConcern(w='majority'))
    
    result = safe_collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route('/count-tesla-primary', methods=['GET'])
def count_tesla_primary():
    """3. Strongly Consistent Read (Primary Only)"""
    primary_collection = base_collection.with_options(read_preference=ReadPreference.PRIMARY)
    count = primary_collection.count_documents({"Make": "TESLA"})
    
    return jsonify({"count": count}), 200

@app.route('/count-bmw-secondary', methods=['GET'])
def count_bmw_secondary():
    """4. Eventually Consistent Analytical Read (Secondary Only)"""
    secondary_collection = base_collection.with_options(read_preference=ReadPreference.SECONDARY)
    count = secondary_collection.count_documents({"Make": "BMW"})
    
    return jsonify({"count": count}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)