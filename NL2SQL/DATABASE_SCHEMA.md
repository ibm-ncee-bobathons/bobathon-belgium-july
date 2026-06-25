# Database Schema Documentation

## Overview
This document describes the actual database schema used in the NL2SQL solution.

## Database: purchase_data

### Table: customer_purchases

Complete customer purchase transaction data with detailed information about customers, products, and order details.

#### Schema Definition

```sql
CREATE TABLE customer_purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    customer_id INT NOT NULL,
    customer_name VARCHAR(100),
    customer_city VARCHAR(80),
    customer_country VARCHAR(80),
    customer_segment VARCHAR(50),
    registration_date DATE,
    purchase_date DATE NOT NULL,
    sales_channel VARCHAR(50),
    product_id VARCHAR(30),
    product_name VARCHAR(100),
    product_category VARCHAR(80),
    brand VARCHAR(80),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'HUF',
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    delivery_status VARCHAR(50),
    is_returned BOOLEAN DEFAULT FALSE,
    rating INT
);
```

#### Column Descriptions

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `purchase_id` | INT | NO | Primary key, auto-increment |
| `order_id` | VARCHAR(30) | NO | Unique order identifier (e.g., 'ORD-UK-2026-0001') |
| `customer_id` | INT | NO | Customer identifier |
| `customer_name` | VARCHAR(100) | YES | Customer full name |
| `customer_city` | VARCHAR(80) | YES | Customer city |
| `customer_country` | VARCHAR(80) | YES | Customer country |
| `customer_segment` | VARCHAR(50) | YES | Customer segment (e.g., 'Premium', 'Standard', 'Basic') |
| `registration_date` | DATE | YES | Customer registration date |
| `purchase_date` | DATE | NO | Date of purchase |
| `sales_channel` | VARCHAR(50) | YES | Sales channel (e.g., 'Online', 'Store', 'Mobile App') |
| `product_id` | VARCHAR(30) | YES | Product identifier (e.g., 'IT-1001') |
| `product_name` | VARCHAR(100) | YES | Product name |
| `product_category` | VARCHAR(80) | YES | Product category (e.g., 'Laptops', 'Phones', 'Accessories') |
| `brand` | VARCHAR(80) | YES | Product brand |
| `quantity` | INT | NO | Quantity purchased |
| `unit_price` | DECIMAL(10,2) | NO | Price per unit |
| `discount_amount` | DECIMAL(10,2) | YES | Discount applied (default 0) |
| `total_amount` | DECIMAL(10,2) | NO | Total amount paid |
| `currency` | VARCHAR(10) | YES | Currency code|
| `payment_method` | VARCHAR(50) | YES | Payment method (e.g., 'Credit Card', 'PayPal', 'Cash') |
| `payment_status` | VARCHAR(50) | YES | Payment status (e.g., 'Paid', 'Pending', 'Failed') |
| `delivery_status` | VARCHAR(50) | YES | Delivery status (e.g., 'Delivered', 'Shipped', 'Processing') |
| `is_returned` | BOOLEAN | YES | Whether the item was returned (default FALSE) |
| `rating` | INT | YES | Customer rating (1-5) |

#### Sample Data

```sql
INSERT INTO customer_purchases VALUES
('ORD-UK-2026-0001', 2001, 'Oliver Smith', 'London', 'United Kingdom', 'Premium', 
 '2024-02-15', '2026-01-05', 'Online', 'IT-1001', 'XPS 13 Laptop', 'Laptops', 
 'Dell', 1, 1199.00, 100.00, 1099.00, 'GBP', 'Credit Card', 'Paid', 'Delivered', 
 FALSE, 5);
```

## Common Query Patterns

### Revenue Analysis

```sql
-- Total revenue by product category
SELECT 
    product_category,
    SUM(total_amount) as total_revenue,
    COUNT(*) as transaction_count
FROM customer_purchases
GROUP BY product_category
ORDER BY total_revenue DESC;

-- Revenue by country
SELECT 
    customer_country,
    currency,
    SUM(total_amount) as total_revenue
FROM customer_purchases
GROUP BY customer_country, currency
ORDER BY total_revenue DESC;
```

### Customer Analysis

```sql
-- Top customers by spending
SELECT 
    customer_id,
    customer_name,
    customer_segment,
    SUM(total_amount) as total_spent,
    COUNT(*) as purchase_count,
    AVG(rating) as avg_rating
FROM customer_purchases
GROUP BY customer_id, customer_name, customer_segment
ORDER BY total_spent DESC
LIMIT 10;

-- Customer segments performance
SELECT 
    customer_segment,
    COUNT(DISTINCT customer_id) as customer_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM customer_purchases
GROUP BY customer_segment
ORDER BY total_revenue DESC;
```

### Product Analysis

```sql
-- Best selling products
SELECT 
    product_name,
    product_category,
    brand,
    SUM(quantity) as total_quantity_sold,
    SUM(total_amount) as total_revenue,
    AVG(rating) as avg_rating
FROM customer_purchases
WHERE rating IS NOT NULL
GROUP BY product_id, product_name, product_category, brand
ORDER BY total_revenue DESC
LIMIT 20;

-- Products by brand performance
SELECT 
    brand,
    COUNT(DISTINCT product_id) as product_count,
    SUM(quantity) as total_units_sold,
    SUM(total_amount) as total_revenue
FROM customer_purchases
GROUP BY brand
ORDER BY total_revenue DESC;
```

### Time Series Analysis

```sql
-- Monthly revenue trend
SELECT 
    DATE_FORMAT(purchase_date, '%Y-%m') as month,
    SUM(total_amount) as monthly_revenue,
    COUNT(*) as transaction_count,
    AVG(total_amount) as avg_transaction_value
FROM customer_purchases
GROUP BY month
ORDER BY month;

-- Daily sales by channel
SELECT 
    purchase_date,
    sales_channel,
    SUM(total_amount) as daily_revenue
FROM customer_purchases
WHERE purchase_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY purchase_date, sales_channel
ORDER BY purchase_date, sales_channel;
```

### Discount Analysis

```sql
-- Impact of discounts
SELECT 
    CASE 
        WHEN discount_amount = 0 THEN 'No Discount'
        WHEN discount_amount <= 50 THEN 'Small (≤50)'
        WHEN discount_amount <= 100 THEN 'Medium (51-100)'
        ELSE 'Large (>100)'
    END as discount_range,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(quantity) as avg_quantity,
    AVG(rating) as avg_rating
FROM customer_purchases
GROUP BY discount_range
ORDER BY discount_range;
```

### Returns Analysis

```sql
-- Return rate by category
SELECT 
    product_category,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_returned THEN 1 ELSE 0 END) as returned_orders,
    ROUND(SUM(CASE WHEN is_returned THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as return_rate_pct
FROM customer_purchases
GROUP BY product_category
ORDER BY return_rate_pct DESC;
```

### Payment Analysis

```sql
-- Revenue by payment method
SELECT 
    payment_method,
    payment_status,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue
FROM customer_purchases
GROUP BY payment_method, payment_status
ORDER BY total_revenue DESC;
```

### Geographic Analysis

```sql
-- Sales by country and city
SELECT 
    customer_country,
    customer_city,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM customer_purchases
GROUP BY customer_country, customer_city
ORDER BY total_revenue DESC
LIMIT 20;
```

## Indexes (Recommended)

For optimal query performance, consider adding these indexes:

```sql
-- Customer lookups
CREATE INDEX idx_customer_id ON customer_purchases(customer_id);
CREATE INDEX idx_customer_segment ON customer_purchases(customer_segment);

-- Product lookups
CREATE INDEX idx_product_id ON customer_purchases(product_id);
CREATE INDEX idx_product_category ON customer_purchases(product_category);
CREATE INDEX idx_brand ON customer_purchases(brand);

-- Time-based queries
CREATE INDEX idx_purchase_date ON customer_purchases(purchase_date);

-- Status tracking
CREATE INDEX idx_payment_status ON customer_purchases(payment_status);
CREATE INDEX idx_delivery_status ON customer_purchases(delivery_status);

-- Composite indexes for common queries
CREATE INDEX idx_date_category ON customer_purchases(purchase_date, product_category);
CREATE INDEX idx_customer_date ON customer_purchases(customer_id, purchase_date);
```

## Data Types and Constraints

### Currency Handling
- Multiple currencies supported (GBP, HUF, USD, EUR, etc.)
- Always specify currency when analyzing revenue
- Consider currency conversion for cross-country comparisons

### Date Ranges
- `registration_date`: Customer account creation
- `purchase_date`: Transaction date (required)

### Boolean Fields
- `is_returned`: Track product returns

### Rating System
- Scale: 1-5 (integer)
- NULL values indicate no rating provided

## Notes for NL2SQL

When generating SQL queries, the system should:

1. **Always specify table name**: Use `customer_purchases` explicitly
2. **Handle NULL values**: Many columns are nullable
3. **Currency awareness**: Group by currency when analyzing revenue across countries
4. **Date formatting**: Use `DATE_FORMAT()` for time-based grouping
5. **Aggregations**: Common metrics include SUM(total_amount), COUNT(*), AVG(rating)
6. **Filtering**: Consider payment_status='Paid' for revenue calculations
7. **Returns**: Exclude returned items when appropriate using `WHERE is_returned = FALSE`

## Example Natural Language Queries

### English
- "Which product category brought in the most revenue?"
- "Top 10 shoppers by total spend"
- "Monthly sales revenue over the last 6 months"
- "Average rating by brand"
- "Return rate by category"
