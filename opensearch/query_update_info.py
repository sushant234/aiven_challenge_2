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

# Check if the OpenSearch connection is successful
if os_client.ping():
    print("Connected to OpenSearch!")
else:
    print("Could not connect to OpenSearch.")
    exit()


def query_recent_updates():
    query = {
        "size": 10,  # Fetch the 10 most recent records
        "query": {
            "match_all": {}  # You can add more specific queries here, such as filtering by classification or other fields
        },
        "sort": [
            {
                "after.created_at": {
                    "order": "desc"  # Sorting by created_at field in descending order to get the latest updates
                }
            }
        ]
    }

    response = os_client.search(index="users", body=query)
    return response['hits']['hits']

# Example of querying recent updates
recent_data = query_recent_updates()

for record in recent_data:
    print(record['_source'])  # Display the actual document (record)
