from kafka import KafkaProducer
from db.mongo import get_producer_collection, log_producer_data, generate_unique_id
from datetime import datetime
import pandas as pd
import asyncio
import random
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_reviews(file_path):
    df = pd.read_csv(file_path)
    return df

async def generate_data(file_path):
    collection = await get_producer_collection()
    df = read_reviews(file_path)
    index = 0
    while index < len(df):
        batch_size = random.randint(1, 5)
        reviews = []
        
        for _ in range(batch_size):
            if index < len(df):
                row = df.iloc[index]
                review_data = {"review": row['review']}
                unique_id = await generate_unique_id(collection)
                timestamp = datetime.utcnow()
                await log_producer_data(collection, unique_id, timestamp)
                reviews.append({"review": row['review'], "producer_timestamp": timestamp.isoformat(), "unique_id": unique_id})
                index += 1

        # Send reviews to Kafka
        for review in reviews:
            producer.send('real-time-data', review)
            print("The data is generated")
        time.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    asyncio.run(generate_data("../IMDB Dataset.csv"))