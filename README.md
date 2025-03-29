
# Real-Time Secure Data Sharing with Aiven PostgreSQL, Kafka, and OpenSearch

## Overview

This project implements a real-time data sharing solution for an organization, enabling secure sharing of sensitive records between different teams. We use the following Aiven services:
- **Aiven PostgreSQL**: Stores sensitive records.
- **Aiven Kafka**: Streams updates from PostgreSQL in real-time using Change Data Capture (CDC).
- **Aiven OpenSearch**: Allows teams to perform advanced searches on the shared data.

This solution enables teams to securely access and visualize data while ensuring data integrity and privacy.

## Products Involved
- **Aiven PostgreSQL**: Centralized storage of sensitive records.
- **Aiven Kafka**: Real-time streaming of database updates using Change Data Capture (CDC).
- **Aiven OpenSearch**: Allows teams to perform advanced searches on the shared data.

## Objectives
- Use **Aiven PostgreSQL** as a central database for storing sensitive records.
- Stream updates in real time to different teams using **Aiven Kafka**.
- Allow teams to perform advanced searches on the shared data using **Aiven OpenSearch**.

## Prerequisites
Before starting, ensure you have the following:
- **Terraform** installed for resource management in Aiven.
- **Python** for automating data insertion into PostgreSQL (optional).
- **Aiven account** with access to PostgreSQL, Kafka, and OpenSearch services.

## Steps to Implement

### 1. Infrastructure Setup with Terraform

Terraform scripts in the `terraform/` directory provision the following infrastructure:
- Kafka cluster
- PostgreSQL instance
- OpenSearch instance (optional)

To set up the infrastructure:
```bash
cd terraform
terraform init
terraform apply
```

### 2. PostgreSQL CDC Configuration
Enable Change Data Capture (CDC) in PostgreSQL and create a logical replication slot.

1. Log into PostgreSQL and create the replication slot and publication:

```sql
SELECT * FROM pg_create_logical_replication_slot('cdc_slot', 'pgoutput');
CREATE PUBLICATION cdc_pub FOR TABLE users;
```

2. Set up the Debezium PostgreSQL connector to capture changes from PostgreSQL and stream them to Kafka.

### 3. Insert Data and Stream Changes to Kafka
Use the following Python inset_user.py script to insert records into database:
Go inside database folder and run

```bash 
    pip3 install -r requirements.txt
    python3 inset_user.py
```

Debezium will detect this change and stream it to Kafka.

### 4. Set Up Kafka Consumer and Ingest Data into OpenSearch
You can build a Kafka consumer or use an OpenSearch connector to consume data from Kafka and store it into OpenSearch. Go inside kafka folder and run

```bash
# Kafka Consumer
python3 consumer_data_classification.py
```

### 5. Visualize Data in OpenSearch Dashboards
Once the data is in OpenSearch, you can use **OpenSearch Dashboards** visualize the data and track updates in real-time.

1. Go to the OpenSearch Dashboards interface.
2. Define an index pattern (e.g., `postgres.public.users`).
3. Use the dashboards to visualize the data and track changes over time.

### 6. Query OpenSearch
You can query OpenSearch to retrieve updated information, Run the following script from opensearch folder:

```bash
    python3 query_update_info.py
```

## Bonus: Secure Data Classification
To enhance security, you can handle two types of data:
- **Public Data**: Can be shared openly.
- **Private Data**: Should be encrypted or masked before being shared.

Configure roles in security/config.yml to control access to public and private data in OpenSearch by defining roles like public_user and private_user with appropriate index privileges. Assign these roles to users to grant access based on their data access needs.Run the following script from opensearch folder:

```bash
    python3 advance_query_mechanism.py
```

## Conclusion
This solution ensures that different teams in your organization can securely share and visualize data in real time using Aiven services. PostgreSQL stores sensitive records, Kafka streams updates, and OpenSearch provides advanced search and visualization capabilities.

## Requirements
- **Terraform**: For provisioning and managing Aiven services.
- **Python**: Optional, for automating data insertion into PostgreSQL.
- **Aiven Account**: To provision and manage PostgreSQL, Kafka, and OpenSearch services.
