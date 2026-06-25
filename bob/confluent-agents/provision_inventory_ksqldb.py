#!/usr/bin/env python3
"""Provision a ksqlDB application for inventory availability in Confluent Cloud."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

DEFAULT_SOURCE_TOPIC: Final[str] = "inventory.transactions"
DEFAULT_STREAM_NAME: Final[str] = "INVENTORY_TRANSACTIONS"
DEFAULT_TABLE_NAME: Final[str] = "INVENTORY_AVAILABILITY"
DEFAULT_KSQLDB_CLUSTER_NAME: Final[str] = "inventory-ksqldb"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a ksqlDB cluster and deploy inventory availability stream/table "
            "statements using the Confluent CLI."
        )
    )
    parser.add_argument(
        "--cluster-name",
        default=os.getenv("CONFLUENT_KSQLDB_CLUSTER_NAME", DEFAULT_KSQLDB_CLUSTER_NAME),
        help="Name for the ksqlDB cluster/app.",
    )
    parser.add_argument(
        "--source-topic",
        default=DEFAULT_SOURCE_TOPIC,
        help="Kafka topic containing inventory transactions.",
    )
    parser.add_argument(
        "--stream-name",
        default=DEFAULT_STREAM_NAME,
        help="ksqlDB stream name for the transactions source.",
    )
    parser.add_argument(
        "--table-name",
        default=DEFAULT_TABLE_NAME,
        help="ksqlDB table name for aggregated availability.",
    )
    parser.add_argument(
        "--sql-file",
        default="inventory_availability.sql",
        help="Path to write the generated ksqlDB statements.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate SQL and print commands without executing the Confluent CLI.",
    )
    return parser.parse_args()


def load_required_env() -> dict[str, str]:
    load_dotenv()
    env = {
        "CONFLUENT_ENVIRONMENT_ID": os.getenv("CONFLUENT_ENVIRONMENT_ID", ""),
        "CONFLUENT_KAFKA_CLUSTER_ID": os.getenv("CONFLUENT_KAFKA_CLUSTER_ID", ""),
    }
    missing = [key for key, value in env.items() if not value]
    if missing:
        raise ValueError(f"Missing required environment values: {', '.join(missing)}")
    return env


def ensure_confluent_cli() -> None:
    if not shutil_which("confluent"):
        raise RuntimeError(
            "Confluent CLI is not installed or not on PATH. Install it before running this script."
        )


def shutil_which(command: str) -> str | None:
    from shutil import which

    return which(command)


def run_command(command: list[str], dry_run: bool = False) -> subprocess.CompletedProcess[str] | None:
    printable = " ".join(shlex.quote(part) for part in command)
    print(f"$ {printable}")
    if dry_run:
        return None

    return subprocess.run(command, check=True, text=True, capture_output=True)


def generate_sql(source_topic: str, stream_name: str, table_name: str) -> str:
    return f"""CREATE STREAM IF NOT EXISTS {stream_name} (
    sku STRING,
    branch STRING,
    quantity INTEGER,
    transaction_type STRING
) WITH (
    KAFKA_TOPIC='{source_topic}',
    VALUE_FORMAT='JSON'
);

CREATE TABLE IF NOT EXISTS {table_name}
WITH (
    KAFKA_TOPIC='inventory.availability',
    VALUE_FORMAT='JSON'
) AS
SELECT
    sku,
    branch,
    SUM(quantity) AS available_quantity
FROM {stream_name}
WHERE transaction_type IN ('Addition', 'SALE')
GROUP BY sku, branch
EMIT CHANGES;
"""


def write_sql_file(path: str, sql: str) -> Path:
    sql_path = Path(path)
    sql_path.write_text(sql, encoding="utf-8")
    return sql_path


def create_ksqldb_cluster(cluster_name: str, env_id: str, kafka_cluster_id: str, dry_run: bool) -> str | None:
    command = [
        "confluent",
        "ksql",
        "cluster",
        "create",
        cluster_name,
        "--environment",
        env_id,
        "--cluster",
        kafka_cluster_id,
        "--output",
        "json",
    ]

    try:
        result = run_command(command, dry_run=dry_run)
        if dry_run or result is None:
            return None
        if result.stdout:
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr or ""
        stdout = exc.stdout or ""
        combined = f"{stdout}\n{stderr}".strip()
        if "already exists" in combined.lower():
            print("ksqlDB cluster already exists; continuing.")
            return None
        raise RuntimeError(f"Failed to create ksqlDB cluster: {combined}") from exc


def execute_sql(sql_file: Path, env_id: str, dry_run: bool) -> None:
    command = [
        "confluent",
        "ksql",
        "execute",
        str(sql_file),
        "--environment",
        env_id,
    ]
    result = run_command(command, dry_run=dry_run)
    if result and result.stdout:
        print(result.stdout)
    if result and result.stderr:
        print(result.stderr, file=sys.stderr)


def describe_table(table_name: str, env_id: str, dry_run: bool) -> None:
    command = [
        "confluent",
        "ksql",
        "describe",
        table_name,
        "--environment",
        env_id,
    ]
    result = run_command(command, dry_run=dry_run)
    if result and result.stdout:
        print(result.stdout)
    if result and result.stderr:
        print(result.stderr, file=sys.stderr)


def main() -> None:
    args = parse_args()
    env = load_required_env()
    ensure_confluent_cli()

    sql = generate_sql(args.source_topic, args.stream_name, args.table_name)
    sql_file = write_sql_file(args.sql_file, sql)
    print(f"Wrote ksqlDB statements to {sql_file}")

    create_ksqldb_cluster(
        cluster_name=args.cluster_name,
        env_id=env["CONFLUENT_ENVIRONMENT_ID"],
        kafka_cluster_id=env["CONFLUENT_KAFKA_CLUSTER_ID"],
        dry_run=args.dry_run,
    )
    execute_sql(sql_file, env["CONFLUENT_ENVIRONMENT_ID"], args.dry_run)
    describe_table(args.table_name, env["CONFLUENT_ENVIRONMENT_ID"], args.dry_run)


if __name__ == "__main__":
    main()
