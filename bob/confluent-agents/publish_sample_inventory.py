#!/usr/bin/env python3
"""Publish sample inventory transactions to Confluent Cloud."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Final

from confluent_kafka import Producer
from dotenv import load_dotenv

DEFAULT_TOPIC_NAME: Final[str] = "inventory.transactions"

SAMPLE_MESSAGES: Final[list[dict[str, object]]] = [
    {"sku": "Dell XPS 13", "branch": "Mall Of Egypt", "quantity": 10, "transaction_type": "Addition"},
    {"sku": "Dell XPS 13", "branch": "Mall Of Egypt", "quantity": -3, "transaction_type": "SALE"},
    {"sku": "Dell XPS 13", "branch": "Mall Of Egypt", "quantity": -7, "transaction_type": "SALE"},
    {"sku": "HP Spectre x360", "branch": "Mall Of Egypt", "quantity": 8, "transaction_type": "Addition"},
    {"sku": "HP Spectre x360", "branch": "Mall Of Egypt", "quantity": -2, "transaction_type": "SALE"},
    {"sku": "Lenovo ThinkPad X1", "branch": "Mall Of Egypt", "quantity": 6, "transaction_type": "Addition"},
    {"sku": "Lenovo ThinkPad X1", "branch": "Mall Of Egypt", "quantity": -1, "transaction_type": "SALE"},
    {"sku": "iPhone 15", "branch": "Mall Of Egypt", "quantity": 15, "transaction_type": "Addition"},
    {"sku": "iPhone 15", "branch": "Mall Of Egypt", "quantity": -4, "transaction_type": "SALE"},
    {"sku": "Samsung Galaxy S24", "branch": "Mall Of Egypt", "quantity": 12, "transaction_type": "Addition"},
    {"sku": "Google Pixel 8", "branch": "Dubai Mall", "quantity": 9, "transaction_type": "Addition"},
    {"sku": "Google Pixel 8", "branch": "Dubai Mall", "quantity": -3, "transaction_type": "SALE"},
    {"sku": "Dell XPS 13", "branch": "Dubai Mall", "quantity": 7, "transaction_type": "Addition"},
    {"sku": "Dell XPS 13", "branch": "Dubai Mall", "quantity": -1, "transaction_type": "SALE"},
    {"sku": "HP Spectre x360", "branch": "Dubai Mall", "quantity": 5, "transaction_type": "Addition"},
    {"sku": "Lenovo ThinkPad X1", "branch": "Dubai Mall", "quantity": 4, "transaction_type": "Addition"},
    {"sku": "iPhone 15", "branch": "Dubai Mall", "quantity": 11, "transaction_type": "Addition"},
    {"sku": "Samsung Galaxy S24", "branch": "Dubai Mall", "quantity": 13, "transaction_type": "Addition"},
    {"sku": "Samsung Galaxy S24", "branch": "Dubai Mall", "quantity": -5, "transaction_type": "SALE"},
    {"sku": "Google Pixel 8", "branch": "Mall Of Egypt", "quantity": 10, "transaction_type": "Addition"},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish sample inventory transaction messages to Confluent Cloud."
    )
    parser.add_argument(
        "--topic",
        default=DEFAULT_TOPIC_NAME,
        help=f"Topic name to publish to (default: {DEFAULT_TOPIC_NAME})",
    )
    return parser.parse_args()


def load_config() -> dict[str, str]:
    load_dotenv()
    required = {
        "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS", ""),
        "sasl.username": os.getenv("CONFLUENT_API_KEY", ""),
        "sasl.password": os.getenv("CONFLUENT_API_SECRET", ""),
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(f"Missing required Confluent Cloud settings: {', '.join(missing)}")

    return {
        "bootstrap.servers": required["bootstrap.servers"],
        "security.protocol": os.getenv("CONFLUENT_SECURITY_PROTOCOL", "SASL_SSL"),
        "sasl.mechanisms": os.getenv("CONFLUENT_SASL_MECHANISM", "PLAIN"),
        "sasl.username": required["sasl.username"],
        "sasl.password": required["sasl.password"],
    }


def delivery_report(err, msg) -> None:  # type: ignore[no-untyped-def]
    if err is not None:
        print(f"Delivery failed for key {msg.key()}: {err}", file=sys.stderr)
        raise RuntimeError(err)


def publish_messages(topic: str) -> None:
    producer = Producer(load_config())

    for index, message in enumerate(SAMPLE_MESSAGES, start=1):
        key = f"{message['sku']}|{message['branch']}"
        payload = json.dumps(message)
        producer.produce(
            topic=topic,
            key=key,
            value=payload,
            on_delivery=delivery_report,
        )
        producer.poll(0)
        print(f"Queued message {index:02d}: {payload}")

    producer.flush()
    print(f"Published {len(SAMPLE_MESSAGES)} messages to '{topic}'.")


def main() -> None:
    args = parse_args()
    publish_messages(args.topic)


if __name__ == "__main__":
    main()
