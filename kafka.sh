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