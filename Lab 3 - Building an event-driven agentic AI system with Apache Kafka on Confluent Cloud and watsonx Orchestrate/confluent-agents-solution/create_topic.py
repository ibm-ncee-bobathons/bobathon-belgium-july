#!/usr/bin/env python3
"""
Create a Kafka topic on Confluent Cloud with configurable partitions and retention.
"""

import os
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_topic():
    """Create the inventory_transactions topic with configured settings."""
    
    # Get configuration from environment variables
    bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
    sasl_username = os.getenv('SASL_USERNAME')
    sasl_password = os.getenv('SASL_PASSWORD')
    topic_name = os.getenv('TOPIC_NAME', 'inventory_transactions')
    num_partitions = int(os.getenv('NUM_PARTITIONS', '1'))
    retention_ms = os.getenv('RETENTION_MS', '-1')
    
    # Validate required environment variables
    if not all([bootstrap_servers, sasl_username, sasl_password]):
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    # Configure the Admin Client
    admin_config = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password
    }
    
    admin_client = AdminClient(admin_config)
    
    # Define topic configuration
    topic_config = {
        'retention.ms': retention_ms
    }
    
    # Create NewTopic object
    new_topic = NewTopic(
        topic=topic_name,
        num_partitions=num_partitions,
        replication_factor=3,  # Confluent Cloud default
        config=topic_config
    )
    
    # Create the topic
    print(f"Creating topic '{topic_name}' with {num_partitions} partition(s) and retention {retention_ms}ms...")
    
    fs = admin_client.create_topics([new_topic])
    
    # Wait for the operation to complete
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"✓ Topic '{topic}' created successfully!")
            print(f"  - Partitions: {num_partitions}")
            print(f"  - Retention: {retention_ms}ms {'(infinite)' if retention_ms == '-1' else ''}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"⚠ Topic '{topic}' already exists.")
            else:
                print(f"✗ Failed to create topic '{topic}': {e}")
                raise

if __name__ == "__main__":
    try:
        create_topic()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# Made with Bob
