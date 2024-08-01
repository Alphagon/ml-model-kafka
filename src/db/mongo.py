from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
import uuid
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

producer_logs_collection = None
consumer_logs_collection = None

async def get_producer_collection():
    global producer_logs_collection
    producer_logs_collection = await get_database_and_collection(client, mongo_db_name, mongo_collection_producer_name)
    return producer_logs_collection

async def get_consumer_collection():
    global consumer_logs_collection
    consumer_logs_collection = await get_database_and_collection(client, mongo_db_name, mongo_collection_consumer_name)
    return consumer_logs_collection

async def unique_id_exists(collection, unique_id):
    count = await collection.count_documents({"_id": unique_id})
    return count > 0

async def generate_unique_id(collection):
    while True:
        unique_id = str(uuid.uuid4())
        if not await unique_id_exists(collection, unique_id):
            return unique_id

async def log_producer_data(collection, unique_id, timestamp):
    await collection.insert_one({
        "_id": unique_id,
        "producer_timestamp": timestamp
    })

async def log_consumer_data(collection, review, prediction, consumer_timestamp, unique_id):
    await collection.insert_one({
        "_id": unique_id,
        "review": review,
        "prediction": prediction,
        "consumer_timestamp": consumer_timestamp
    })