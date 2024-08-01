# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
import os

# Loading environment variables from .envfile
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path)

#MongoDB setup
mongo_uri = os.getenv('MONGO_URL')
mongo_db_name = os.getenv('MONGO_DATABASE_NAME')
mongo_collection_producer_name = os.getenv("MONGO_COLLECTION_PRODUCER_NAME")
mongo_collection_consumer_name = os.getenv("MONGO_COLLECTION_CONSUMER_NAME")

client = AsyncIOMotorClient(mongo_uri)


async def get_database_and_collection(client, db_name, collection_name):
    db_list = await client.list_database_names()
    if db_name not in db_list:
        db = client[db_name]
        await db.create_collection(collection_name)
        print(f"Database {db_name} and collection {collection_name} created")
    else:
        db = client[db_name]
        collection_list = await db.list_collection_names()
        if collection_name not in collection_list:
            await db.create_collection(collection_name)
            print(f"Collection {collection_name} created in database {db_name}")
        
    return db[collection_name]

logs_collection = None

async def initalize_logs_collection(mongo_collection_name):
    global logs_collection
    logs_collection = await get_database_and_collection(client, mongo_db_name, mongo_collection_name)

async def log_producer_data(collection, data, timestamp):
    await collection.insert_one({
        "data": data,
        "timestamp": timestamp
    })

def create_log_entry(request, review_text, status, error_details=None):
    log_entry = {
        "client": request.client.host,
        "review": review_text,
        "path": request.url.path,
        "method": request.method,
        "headers": dict(request.headers),
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }
    if error_details:
        log_entry["error_details"] = error_details
    return log_entry