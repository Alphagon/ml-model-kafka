from kafka import KafkaConsumer
import json
from services import make_predictions

consumer = KafkaConsumer(
    'real-time-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_data():
    for message in consumer:
        data = message.value
        review = data['review']
        prediction = make_predictions(review)
        print(f"Review: {review}, Prediction: {prediction}")

if __name__ == "__main__":
    process_data()