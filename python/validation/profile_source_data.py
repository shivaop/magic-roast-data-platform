import csv
from pathlib import Path


DATA_DIR = Path("data/sample")


def read_csv(filename):
    with (DATA_DIR / filename).open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


customers = read_csv("customers.csv")
products = read_csv("products.csv")
orders = read_csv("orders.csv")
order_items = read_csv("order_items.csv")


customer_ids = {
    customer["customer_id"]
    for customer in customers
}

product_ids = {
    product["product_id"]
    for product in products
}

order_ids = {
    order["order_id"]
    for order in orders
}


invalid_order_customers = [
    order
    for order in orders
    if order["customer_id"] not in customer_ids
]

invalid_order_items = [
    item
    for item in order_items
    if item["order_id"] not in order_ids
]

invalid_products = [
    item
    for item in order_items
    if item["product_id"] not in product_ids
]


print("SOURCE DATA PROFILE")
print("-------------------")

print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
print(f"Order items: {len(order_items)}")

print("\nRELATIONSHIP CHECKS")
print("-------------------")

print(
    f"Orders with invalid customers: "
    f"{len(invalid_order_customers)}"
)

print(
    f"Order items with invalid orders: "
    f"{len(invalid_order_items)}"
)

print(
    f"Order items with invalid products: "
    f"{len(invalid_products)}"
)