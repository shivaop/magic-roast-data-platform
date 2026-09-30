# Magic Roast Coffee — Source Data Dictionary

## Purpose

This document defines the structure, meaning, and expected quality
rules for the source datasets used by the Magic Roast Data Platform.

The source datasets represent the operational business data used to
build the analytical data platform.

---

# 1. Customers

### Grain

One row represents one customer.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| customer_id | VARCHAR | Unique business identifier for a customer | Required and unique |
| first_name | VARCHAR | Customer first name | Required |
| last_name | VARCHAR | Customer last name | Required |
| email | VARCHAR | Customer email address | Required |
| city | VARCHAR | Customer city | Optional |
| state | VARCHAR | Customer state | Optional |
| signup_date | DATE | Date the customer registered | Required |

---

# 2. Products

### Grain

One row represents one product.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| product_id | VARCHAR | Unique business identifier for a product | Required and unique |
| product_name | VARCHAR | Name of the product | Required |
| category | VARCHAR | Product category | Required |
| unit_price | NUMBER | Current selling price | Must be greater than 0 |
| stock_quantity | INTEGER | Current available inventory | Must be >= 0 |
| product_status | VARCHAR | Current product status | ACTIVE or INACTIVE |

---

# 3. Orders

### Grain

One row represents one customer order.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| order_id | VARCHAR | Unique identifier for an order | Required and unique |
| customer_id | VARCHAR | Customer who placed the order | Required; must exist in customers |
| order_date | DATE | Date the order was created | Required |
| campaign_id | VARCHAR | Marketing campaign associated with the order | Optional |
| order_status | VARCHAR | Current order status | COMPLETED, CANCELLED, or PENDING |
| total_amount | NUMBER | Total monetary value of the order | Must be >= 0 |

---

# 4. Order Items

### Grain

One row represents one product within an order.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| order_item_id | VARCHAR | Unique identifier for an order item | Required and unique |
| order_id | VARCHAR | Order containing the item | Required; must exist in orders |
| product_id | VARCHAR | Product purchased | Required; must exist in products |
| quantity | INTEGER | Number of units purchased | Must be greater than 0 |
| unit_price | NUMBER | Price of the product at purchase time | Must be greater than 0 |

---

# 5. Payments

### Grain

One row represents one payment transaction.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| payment_id | VARCHAR | Unique payment identifier | Required and unique |
| order_id | VARCHAR | Order associated with the payment | Required; must exist in orders |
| payment_date | DATE | Date the payment was processed | Required |
| payment_method | VARCHAR | Method used for payment | UPI, CARD, COD, etc. |
| payment_status | VARCHAR | Payment transaction status | SUCCESS, FAILED, or REFUNDED |
| amount | NUMBER | Amount associated with the payment | Must be >= 0 |

---

# 6. Marketing

### Grain

One row represents one marketing campaign.

| Column | Data Type | Description | Expected Rule |
|---|---|---|---|
| campaign_id | VARCHAR | Unique campaign identifier | Required and unique |
| campaign_name | VARCHAR | Name of the marketing campaign | Required |
| channel | VARCHAR | Marketing channel | Instagram, Google, Email, etc. |
| start_date | DATE | Campaign start date | Required |
| end_date | DATE | Campaign end date | Required |
| budget | NUMBER | Campaign budget | Must be >= 0 |
| conversions | INTEGER | Number of conversions attributed to campaign | Must be >= 0 |

---

# Data Quality Expectations

The platform should detect and handle:

- Duplicate records
- Missing primary/business identifiers
- Missing foreign keys
- Orphan records
- Invalid dates
- Invalid prices
- Invalid quantities
- Invalid statuses
- Unexpected NULL values
- Missing payments
- Duplicate orders
- Referential integrity violations

---

# Source Relationships

```text
CUSTOMERS
    |
    | 1 → many
    |
ORDERS
    |
    +------ 1 → many ------ ORDER_ITEMS ------ many → 1 ------ PRODUCTS
    |
    +------ 1 → many ------ PAYMENTS
    |
    +------ many → 1 ------ MARKETING