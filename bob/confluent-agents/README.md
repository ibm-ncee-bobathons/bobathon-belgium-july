# Confluent Cloud Inventory Demo

This project provisions a Confluent Cloud topic and ksqlDB objects for inventory transactions and inventory availability.

## Files

- [`create_topic.py`](bob/confluent-agents/create_topic.py) — creates a topic with configurable partition count and retention.
- [`provision_inventory_ksqldb.py`](bob/confluent-agents/provision_inventory_ksqldb.py) — creates a ksqlDB cluster with the Confluent CLI and deploys the inventory stream/table.
- [`publish_sample_inventory.py`](bob/confluent-agents/publish_sample_inventory.py) — publishes 20 sample JSON inventory transaction messages.
- [`validate_inventory_ksqldb.py`](bob/confluent-agents/validate_inventory_ksqldb.py) — queries ksqlDB and validates expected aggregated availability.
- [`inventory_availability.sql`](bob/confluent-agents/inventory_availability.sql) — ksqlDB statements that define the JSON stream and aggregated availability table.
- [`.env.example`](bob/confluent-agents/.env.example) — fill this in with your Confluent Cloud connection details, then copy it to [`.env`](bob/confluent-agents/.env).

## Inventory event model

The source topic [`inventory.transactions`](bob/confluent-agents/inventory_availability.sql) is expected to receive JSON messages with these fields:

- `sku`
- `branch`
- `quantity`
- `transaction_type`

`transaction_type` rules:

- `Addition` — positive quantity added to stock
- `SALE` — negative quantity from a point-of-sale transaction

Example JSON event:

```json
{
  "sku": "Dell XPS 13",
  "branch": "Mall Of Egypt",
  "quantity": -2,
  "transaction_type": "SALE"
}
```

## Sample data set

[`publish_sample_inventory.py`](bob/confluent-agents/publish_sample_inventory.py) publishes exactly 20 events across:

- branches: `Mall Of Egypt`, `Dubai Mall`
- laptop SKUs: `Dell XPS 13`, `HP Spectre x360`, `Lenovo ThinkPad X1`
- mobile SKUs: `iPhone 15`, `Samsung Galaxy S24`, `Google Pixel 8`

Expected aggregated balances after all messages are processed:

| SKU | Branch | available_quantity |
| --- | --- | ---: |
| Dell XPS 13 | Mall Of Egypt | 0 |
| HP Spectre x360 | Mall Of Egypt | 6 |
| Lenovo ThinkPad X1 | Mall Of Egypt | 5 |
| iPhone 15 | Mall Of Egypt | 11 |
| Samsung Galaxy S24 | Mall Of Egypt | 12 |
| Google Pixel 8 | Mall Of Egypt | 10 |
| Dell XPS 13 | Dubai Mall | 6 |
| HP Spectre x360 | Dubai Mall | 5 |
| Lenovo ThinkPad X1 | Dubai Mall | 4 |
| iPhone 15 | Dubai Mall | 11 |
| Samsung Galaxy S24 | Dubai Mall | 8 |
| Google Pixel 8 | Dubai Mall | 6 |

This intentionally leaves [`Dell XPS 13`](bob/confluent-agents/publish_sample_inventory.py:17) at `0` quantity in `Mall Of Egypt`.

## Setup

1. Install Python dependencies:

```bash
pip install confluent-kafka python-dotenv
```

2. Install the Confluent CLI and authenticate it:

```bash
brew install confluentinc/tap/cli
confluent login
```

3. Copy the environment template and add your values:

```bash
cp .env.example .env
```

## Required environment variables

For topic creation and publishing:

- `CONFLUENT_BOOTSTRAP_SERVERS`
- `CONFLUENT_API_KEY`
- `CONFLUENT_API_SECRET`

For ksqlDB provisioning and validation:

- `CONFLUENT_ENVIRONMENT_ID`
- `CONFLUENT_KAFKA_CLUSTER_ID`
- `CONFLUENT_KSQLDB_CLUSTER_NAME` (optional, default `inventory-ksqldb`)

Optional:

- `CONFLUENT_SECURITY_PROTOCOL` (default `SASL_SSL`)
- `CONFLUENT_SASL_MECHANISM` (default `PLAIN`)

## Create the topic

```bash
python create_topic.py --topic inventory.transactions --partitions 1 --retention-ms -1
```

## Provision ksqlDB inventory aggregation

This creates:

- stream [`INVENTORY_TRANSACTIONS`](bob/confluent-agents/inventory_availability.sql)
- table [`INVENTORY_AVAILABILITY`](bob/confluent-agents/inventory_availability.sql)
- sink topic `inventory.availability` in JSON format

Run:

```bash
python provision_inventory_ksqldb.py
```

Dry run to preview CLI commands without executing them:

```bash
python provision_inventory_ksqldb.py --dry-run
```

## Publish the sample messages

```bash
python publish_sample_inventory.py --topic inventory.transactions
```

## Validate ksqlDB processing

```bash
python validate_inventory_ksqldb.py
```

This runs a [`SELECT sku, branch, available_quantity ...`](bob/confluent-agents/validate_inventory_ksqldb.py:63) query through the Confluent CLI and validates the expected 12 aggregated rows.

Dry run:

```bash
python validate_inventory_ksqldb.py --dry-run
```

## Important validation note

[`provision_inventory_ksqldb.py`](bob/confluent-agents/provision_inventory_ksqldb.py), [`validate_inventory_ksqldb.py`](bob/confluent-agents/validate_inventory_ksqldb.py), and actual ksqlDB verification require the external `confluent` CLI binary and a logged-in CLI session.
