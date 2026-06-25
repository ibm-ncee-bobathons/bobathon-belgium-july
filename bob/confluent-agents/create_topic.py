#!/usr/bin/env python3
"""Create a Kafka topic in Confluent Cloud with configurable partitions and retention."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Final

from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

DEFAULT_TOPIC_NAME: Final[str] = "inventory.transactions"
DEFAULT_PARTITIONS: Final[int] = 1
DEFAULT_RETENTION_MS: Final[int] = -1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Confluent Cloud topic with configurable partitions and retention."
    )
    parser.add_argument(
        "--topic",
        default=DEFAULT_TOPIC_NAME,
        help=f"Topic name to create (default: {DEFAULT_TOPIC_NAME})",
    )
    parser.add_argument(
        "--partitions",
        type=int,
        default=DEFAULT_PARTITIONS,
        help=f"Number of partitions (default: {DEFAULT_PARTITIONS})",
    )
    parser.add_argument(
        "--retention-ms",
        type=int,
        default=DEFAULT_RETENTION_MS,
        help=(
            "Topic retention in milliseconds. Use -1 for infinite retention "
            f"(default: {DEFAULT_RETENTION_MS})."
        ),
    )
    return parser.parse_args()


def load_config() -> dict[str, str]:
    load_dotenv()

    required_env_vars = {
        "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS", ""),
        "sasl.username": os.getenv("CONFLUENT_API_KEY", ""),
        "sasl.password": os.getenv("CONFLUENT_API_SECRET", ""),
    }

    missing = [name for name, value in required_env_vars.items() if not value]
    if missing:
        missing_display = ", ".join(missing)
        raise ValueError(
            "Missing required Confluent Cloud settings in environment: "
            f"{missing_display}"
        )

    return {
        "bootstrap.servers": required_env_vars["bootstrap.servers"],
        "security.protocol": os.getenv("CONFLUENT_SECURITY_PROTOCOL", "SASL_SSL"),
        "sasl.mechanisms": os.getenv("CONFLUENT_SASL_MECHANISM", "PLAIN"),
        "sasl.username": required_env_vars["sasl.username"],
        "sasl.password": required_env_vars["sasl.password"],
    }


def create_topic(topic_name: str, partitions: int, retention_ms: int) -> None:
    if partitions < 1:
        raise ValueError("Partitions must be at least 1.")

    config = load_config()
    admin_client = AdminClient(config)

    new_topic = NewTopic(
        topic=topic_name,
        num_partitions=partitions,
        config={"retention.ms": str(retention_ms)},
    )

    futures = admin_client.create_topics([new_topic])
    future = futures[topic_name]

    try:
        future.result()
        print(
            f"Created topic '{topic_name}' with {partitions} partition(s) "
            f"and retention.ms={retention_ms}."
        )
    except Exception as exc:  # confluent_kafka raises KafkaException subclasses here
        print(f"Failed to create topic '{topic_name}': {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main() -> None:
    args = parse_args()
    create_topic(
        topic_name=args.topic,
        partitions=args.partitions,
        retention_ms=args.retention_ms,
    )


if __name__ == "__main__":
    main()
