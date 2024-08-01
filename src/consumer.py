from kafka import KafkaConsumer
import asyncio
from datetime import datetime
from db.mongo import get_consumer_collection, log_consumer_data
from services import make_predictions
import json

consumer = KafkaConsumer(
    'real-time-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

async def process_data():
    collection = await get_consumer_collection()
    for message in consumer:
        data = message.value
        review = data['review']
        unique_id = data['unique_id']
        consumer_timestamp = datetime.utcnow().isoformat()
        prediction = make_predictions(review)
        await log_consumer_data(collection, review, prediction, consumer_timestamp, unique_id)
        # print(f"Review: {review}, Prediction: {prediction}, Producer Timestamp: {producer_timestamp}, Consumer Timestamp: {consumer_timestamp}, Unique ID: {unique_id}")

if __name__ == "__main__":
    asyncio.run(process_data())