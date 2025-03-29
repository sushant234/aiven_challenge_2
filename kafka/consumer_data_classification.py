from confluent_kafka import Consumer, KafkaException, KafkaError # type: ignore
import os, json
from dotenv import load_dotenv
import sys
from opensearchpy import OpenSearch  # type: ignore
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# OpenSearch Configuration
os_client = OpenSearch(
    hosts=[{'host': os.getenv("OS_HOST"), 'port': int(os.getenv("OS_PORT"))}],
    http_auth=(os.getenv("OS_USER"), os.getenv("OS_PASSWORD")),
    use_ssl=True,
    verify_certs=True,
    ca_certs=None  # Adjust this if you are using a custom CA certificate
)

# Check if the OpenSearch connection is successful
if os_client.ping():
    print("Connected to OpenSearch!")
else:
    print("Could not connect to OpenSearch.")
    exit()


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
                message = json.loads(msg.value().decode('utf-8'))
                print("messages: ", message)
                insert_into_opensearch(message)

    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting...")
    finally:
        # Close the consumer gracefully
        consumer.close()

# Function to insert data into OpenSearch
def insert_into_opensearch(data):
    response = os_client.index(index="users", body=data)  # Use 'body' instead of 'document'
    print(f"Inserted data into OpenSearch: {response}")


if __name__ == "__main__":
    consume_messages()

