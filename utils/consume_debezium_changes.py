from confluent_kafka import Consumer, KafkaException, KafkaError # type: ignore
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Configuration for the Kafka consumer
conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER"),
    'group.id': "debezium-consumer-group",
    'auto.offset.reset': 'earliest',
    'security.protocol': 'SSL',
    'ssl.ca.location': os.getenv("KAFKA_CA_CERT"),
    'ssl.certificate.location': os.getenv("KAFKA_CERT"),
    'ssl.key.location': os.getenv("KAFKA_KEY"),
}

# Kafka topic to monitor (replace with your Debezium topic name)
topic = 'postgres.public.users'

# Create Kafka consumer instance
consumer = Consumer(conf)

# Function to handle the consumption of messages
def consume_messages():
    try:
        # Subscribe to the topic
        consumer.subscribe([topic])

        print(f"Listening for changes on topic '{topic}'...")

        while True:
            # Poll for messages
            msg = consumer.poll(timeout=1.0)  # Timeout of 1 second

            if msg is None:
                continue  # No message, keep polling
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached
                    print(f"End of partition reached for {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Successfully received a message
                print(f"Received message: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting...")
    finally:
        # Close the consumer gracefully
        consumer.close()

if __name__ == "__main__":
    consume_messages()
