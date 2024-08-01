import pandas as pd
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_reviews(file_path):
    df = pd.read_csv(file_path)
    return df

def generate_data(file_path):
    df = read_reviews(file_path)
    index = 0
    while index < len(df):
        batch_size = random.randint(1, 5)
        reviews = []
        
        for _ in range(batch_size):
            if index < len(df):
                row = df.iloc[index]
                reviews.append({"review": row['review']})
                index += 1

        # Send reviews to Kafka
        for review in reviews:
            producer.send('real-time-data', review)
            print(f"A review is generated")

        time.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    generate_data("../IMDB Dataset.csv")