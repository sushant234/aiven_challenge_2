import os, json
from dotenv import load_dotenv
import sys
from opensearchpy import OpenSearch  # type: ignore

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

ES_INDEX = "users"

# Check if the OpenSearch connection is successful
if os_client.ping():
    print("Connected to OpenSearch!")
else:
    print("Could not connect to OpenSearch.")
    exit()

# Example query to securely search for public data
def query_public_data():
    query = {
        "query": {
            "term": {
                "after.data_classification": "public"
            }
        }
    }

    response = os_client.search(index=ES_INDEX, body=query)
    return response['hits']['hits']

# Example query to securely search for private data (accessible by private users)
def query_private_data():
    query = {
        "query": {
            "term": {
                "after.data_classification": "private"
            }
        }
    }

    response = os_client.search(index=ES_INDEX, body=query)
    return response['hits']['hits']

# Example query based on user role
user_role = "private_user"  # This could come from your authentication system

if user_role == "public_user":
    data = query_public_data()
elif user_role == "private_user":
    data = query_private_data()
else:
    data = []

print(data)
