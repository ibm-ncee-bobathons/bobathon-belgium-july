#!/usr/bin/env python3
"""
Produce sample inventory transaction messages to the inventory_transactions topic.
"""

import os
import json
import random
from datetime import datetime
from confluent_kafka import Producer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def delivery_report(err, msg):
    """Callback for message delivery reports."""
    if err is not None:
        print(f'✗ Message delivery failed: {err}')
    else:
        print(f'✓ Message delivered to {msg.topic()} [partition {msg.partition()}] at offset {msg.offset()}')

def create_producer():
    """Create and configure the Kafka producer."""
    bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
    sasl_username = os.getenv('SASL_USERNAME')
    sasl_password = os.getenv('SASL_PASSWORD')
    
    if not all([bootstrap_servers, sasl_username, sasl_password]):
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password,
        'client.id': 'inventory-producer'
    }
    
    return Producer(producer_config)

def generate_sample_messages():
    """Generate 20 sample inventory transaction messages."""
    
    branches = ["Mall Of Egypt", "Dubai Mall"]
    laptop_brands = ["Dell XPS 15", "MacBook Pro M3", "Lenovo ThinkPad X1"]
    mobile_brands = ["iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8"]
    
    all_skus = laptop_brands + mobile_brands
    
    messages = []
    
    # Generate initial inventory additions for all products in both branches
    for branch in branches:
        for sku in all_skus:
            # Initial stock addition
            messages.append({
                "sku": sku,
                "branch": branch,
                "quantity": random.randint(10, 50),
                "transaction_type": "ADDITION",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
    
    # Generate some sales transactions
    for _ in range(8):
        branch = random.choice(branches)
        sku = random.choice(all_skus)
        messages.append({
            "sku": sku,
            "branch": branch,
            "quantity": -random.randint(1, 5),
            "transaction_type": "SALE",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    # Make Lenovo ThinkPad X1 have 0 quantity at Mall Of Egypt
    # First add some stock
    messages.append({
        "sku": "Lenovo ThinkPad X1",
        "branch": "Mall Of Egypt",
        "quantity": 5,
        "transaction_type": "ADDITION",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
    
    # Then sell all of it
    messages.append({
        "sku": "Lenovo ThinkPad X1",
        "branch": "Mall Of Egypt",
        "quantity": -5,
        "transaction_type": "SALE",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
    
    return messages[:20]  # Ensure exactly 20 messages

def produce_messages():
    """Produce sample messages to the inventory_transactions topic."""
    
    topic_name = os.getenv('TOPIC_NAME', 'inventory_transactions')
    producer = create_producer()
    
    messages = generate_sample_messages()
    
    print(f"📤 Producing {len(messages)} messages to topic '{topic_name}'...\n")
    
    for i, message in enumerate(messages, 1):
        # Use SKU as the key for partitioning
        key = message['sku']
        value = json.dumps(message)
        
        print(f"Message {i}: {message['transaction_type']} - {message['sku']} @ {message['branch']}: {message['quantity']}")
        
        producer.produce(
            topic=topic_name,
            key=key.encode('utf-8'),
            value=value.encode('utf-8'),
            callback=delivery_report
        )
        
        # Trigger delivery reports
        producer.poll(0)
    
    # Wait for all messages to be delivered
    print(f"\n⏳ Waiting for all messages to be delivered...")
    producer.flush()
    
    print(f"\n✓ All {len(messages)} messages produced successfully!")
    
    # Print summary
    print(f"\n📊 Summary:")
    additions = sum(1 for m in messages if m['transaction_type'] == 'ADDITION')
    sales = sum(1 for m in messages if m['transaction_type'] == 'SALE')
    print(f"  - ADDITION transactions: {additions}")
    print(f"  - SALE transactions: {sales}")
    print(f"  - Branches: Mall Of Egypt, Dubai Mall")
    print(f"  - Laptop SKUs: Dell XPS 15, MacBook Pro M3, Lenovo ThinkPad X1")
    print(f"  - Mobile SKUs: iPhone 15 Pro, Samsung Galaxy S24, Google Pixel 8")
    print(f"  - Note: Lenovo ThinkPad X1 at Mall Of Egypt has 0 inventory (all consumed)")

if __name__ == "__main__":
    try:
        produce_messages()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# Made with Bob
