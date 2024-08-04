# Kafka for Real-Time ML

For this demonstration we'll be using IMDB sentiment classification model. [Keras model]
Below are the steps you need to follow to implement this.

### Insatlling and initalizing Kafka, Zookeeper and Mongo
We will be using kafka and zookeeper to produce and cosumer the fake IMDB data, and Mongo to store the producer and consumer logs in seperate collections.
You can use docker images of Kafka, Zookeeper and Mongo to initate them on your local system.

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

Build the docker using the following command - `sudo docker-compose up --build`

Once the build is complete check if all the images are built properly using the following command - `sudo docker ps`.
You should find three images up and running [Kafka, Zookeeper, and Mongo]

Next create a listener for kafka using the following command
```
docker exec -it <kafka_container_id> /usr/bin/kafka-topics --create --topic real-time-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Replace the kafka_container_id with your container ID and the topic name is "real-time-data"