# Kafka for Real-Time ML

For this demonstration, we'll be using an IMDB sentiment classification model (Keras model). Below are the steps to implement this.

### Insatlling and initalizing Kafka, Zookeeper and Mongo
We will be using Kafka and Zookeeper to produce and consume the fake IMDB data, and MongoDB to store the producer and consumer logs in separate collections. You can use Docker images of Kafka, Zookeeper, and MongoDB to initiate them on your local system.

Write a docker-compose code to build them
```
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  zookeeper:
    image: 'zookeeper:latest'
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - '2181:2181'
    depends_on:
      - mongodb

  kafka:
    image: "confluentinc/cp-kafka:latest"  # Use a compatible Kafka image
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT"
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:9092"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://localhost:9092"  # Change to localhost
      KAFKA_BROKER_ID: "1"
    depends_on:
      - zookeeper
      - mongodb

volumes:
  mongo_data:
```

Build the docker containers using the following command - `sudo docker-compose up --build`

Once the build is complete, check if all the images are built properly using - `sudo docker ps`
You should see three images up and running (Kafka, Zookeeper, and MongoDB).

Next, create a topic for Kafka using the following command
```
docker exec -it <kafka_container_id> /usr/bin/kafka-topics --create --topic real-time-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Replace `<kafka_container_id>` with your container ID. The topic name is `real-time-data`. Now the system is ready to generate dummy data and run predictions on them.

### Creating producer and Consumer Scripts
Create both producer and consumer scripts, you can refer to them in the attached file.

##### producer.py -
The producer script reads reviews from a CSV file, generates unique IDs and timestamps for each review, and logs this data to a MongoDB collection. It sends the reviews to a Kafka topic in random batches with delays. The output is real-time review data messages sent to Kafka.

##### consumer.py - 
The consumer script listens to a Kafka topic for real-time review data messages, deserializes the messages, and processes each review by making predictions. It logs the review, prediction, and timestamps to a MongoDB collection. The output is the logging of processed data with predictions and timestamps.

To run the both producer and consumer scripts simultaneously create a bash file to automate it
```
#!/bin/bash

source ~/home/yravi/Documents/onelab/onelab/bin/activate

python3 src/producer.py &
producer_pid=$!         # Get the PID of the producer

python3 src/consumer.py &
consumer_pid=$!         # Get the PID of the consumer

# Function to kill the processes
cleanup() {
    echo "Killing producer and consumer..."
    kill $producer_pid $consumer_pid
    exit
}

# Trap SIGINT (Ctrl + C) and call cleanup
trap cleanup SIGINT

# Wait for both processes to finish
wait

echo "Both producer and consumer have completed."
```

Using the command `bash kafka.sh` you can run both the files.

### Accessing MongoDB
To verify that MongoDB is logging data, access the MongoDB command line with:

`sudo docker exec -it mongo mongosh`

From the MongoDB command line, you can run the following commands:
- Switch to the logging database: `use kafka_real_time_data`
- Show collections: `show collections`
- Retrieve all logs from producer: `db.producer_logs.find()`
- Retrieve all logs from consumer: `db.consumer_logs.find()`
- Retrieve the latest log entry of producer: `db.producer_logs.find().sort({ _id: -1 }).limit(1)`
Similarly you can do it for consumer too

###### PS: You can change the environment variables for MongoDB from the .env file.