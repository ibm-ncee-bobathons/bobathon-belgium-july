#!/usr/bin/env python3
"""Validate ksqlDB inventory availability results with the Confluent CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

DEFAULT_TABLE_NAME: Final[str] = "INVENTORY_AVAILABILITY"
EXPECTED_AVAILABILITY: Final[dict[tuple[str, str], int]] = {
    ("Dell XPS 13", "Mall Of Egypt"): 0,
    ("HP Spectre x360", "Mall Of Egypt"): 6,
    ("Lenovo ThinkPad X1", "Mall Of Egypt"): 5,
    ("iPhone 15", "Mall Of Egypt"): 11,
    ("Samsung Galaxy S24", "Mall Of Egypt"): 12,
    ("Google Pixel 8", "Mall Of Egypt"): 10,
    ("Google Pixel 8", "Dubai Mall"): 6,
    ("Dell XPS 13", "Dubai Mall"): 6,
    ("HP Spectre x360", "Dubai Mall"): 5,
    ("Lenovo ThinkPad X1", "Dubai Mall"): 4,
    ("iPhone 15", "Dubai Mall"): 11,
    ("Samsung Galaxy S24", "Dubai Mall"): 8,
}

ROW_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\|\s*(?P<sku>[^|]+?)\s*\|\s*(?P<branch>[^|]+?)\s*\|\s*(?P<available_quantity>-?\d+)\s*\|"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the INVENTORY_AVAILABILITY ksqlDB table output."
    )
    parser.add_argument(
        "--table-name",
        default=DEFAULT_TABLE_NAME,
        help=f"ksqlDB table name to query (default: {DEFAULT_TABLE_NAME})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated Confluent CLI command without executing it.",
    )
    return parser.parse_args()


def load_required_env() -> dict[str, str]:
    load_dotenv()
    environment_id = os.getenv("CONFLUENT_ENVIRONMENT_ID", "")
    if not environment_id:
        raise ValueError("Missing required environment value: CONFLUENT_ENVIRONMENT_ID")
    return {"CONFLUENT_ENVIRONMENT_ID": environment_id}


def run_query(table_name: str, environment_id: str, dry_run: bool) -> str:
    query = (
        f"SELECT sku, branch, available_quantity FROM {table_name} EMIT CHANGES LIMIT 12;"
    )
    command = [
        "confluent",
        "ksql",
        "query",
        query,
        "--environment",
        environment_id,
    ]
    printable = " ".join(shlex.quote(part) for part in command)
    print(f"$ {printable}")
    if dry_run:
        return ""

    result = subprocess.run(command, check=True, text=True, capture_output=True)
    output = (result.stdout or "") + (result.stderr or "")
    print(output)
    return output


def parse_rows(output: str) -> dict[tuple[str, str], int]:
    actual: dict[tuple[str, str], int] = {}
    for match in ROW_PATTERN.finditer(output):
        sku = match.group("sku").strip()
        branch = match.group("branch").strip()
        available_quantity = int(match.group("available_quantity"))
        actual[(sku, branch)] = available_quantity
    return actual


def validate_results(actual: dict[tuple[str, str], int]) -> None:
    missing = []
    mismatched = []

    for key, expected_quantity in EXPECTED_AVAILABILITY.items():
        if key not in actual:
            missing.append(key)
            continue
        actual_quantity = actual[key]
        if actual_quantity != expected_quantity:
            mismatched.append((key, expected_quantity, actual_quantity))

    if missing or mismatched:
        if missing:
            print("Missing rows:", file=sys.stderr)
            for sku, branch in missing:
                print(f"- {sku} @ {branch}", file=sys.stderr)
        if mismatched:
            print("Mismatched rows:", file=sys.stderr)
            for (sku, branch), expected_quantity, actual_quantity in mismatched:
                print(
                    f"- {sku} @ {branch}: expected {expected_quantity}, got {actual_quantity}",
                    file=sys.stderr,
                )
        raise SystemExit(1)

    print("ksqlDB validation successful. Aggregated availability matches expected results.")


def main() -> None:
    args = parse_args()
    env = load_required_env()
    output = run_query(args.table_name, env["CONFLUENT_ENVIRONMENT_ID"], args.dry_run)
    if args.dry_run:
        return
    actual = parse_rows(output)
    validate_results(actual)


if __name__ == "__main__":
    main()
