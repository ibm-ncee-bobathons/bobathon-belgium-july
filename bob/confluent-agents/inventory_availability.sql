CREATE STREAM IF NOT EXISTS INVENTORY_TRANSACTIONS (
    sku STRING,
    branch STRING,
    quantity INTEGER,
    transaction_type STRING
) WITH (
    KAFKA_TOPIC='inventory.transactions',
    VALUE_FORMAT='JSON'
);

CREATE TABLE IF NOT EXISTS INVENTORY_AVAILABILITY
WITH (
    KAFKA_TOPIC='inventory.availability',
    VALUE_FORMAT='JSON'
) AS
SELECT
    sku,
    branch,
    SUM(quantity) AS available_quantity
FROM INVENTORY_TRANSACTIONS
WHERE transaction_type IN ('Addition', 'SALE')
GROUP BY sku, branch
EMIT CHANGES;
