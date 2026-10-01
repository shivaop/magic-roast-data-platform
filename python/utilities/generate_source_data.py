import csv
import random
from datetime import date, timedelta
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------

OUTPUT_DIR = Path("data/sample")

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 15
NUM_ORDERS = 2000

random.seed(42)


# -----------------------------
# Sample business data
# -----------------------------

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan",
    "Ishaan", "Kabir", "Rahul", "Siddharth", "Kunal",
    "Ananya", "Aisha", "Isha", "Priya", "Sneha",
    "Riya", "Neha", "Kavya", "Meera", "Pooja"
]

LAST_NAMES = [
    "Sharma", "Patil", "Deshmukh", "Joshi", "Kulkarni",
    "Bhosale", "Pawar", "Jadhav", "More", "Chavan",
    "Singh", "Verma", "Gupta", "Mehta", "Shah"
]

CITIES = [
    ("Pune", "Maharashtra"),
    ("Mumbai", "Maharashtra"),
    ("Kolhapur", "Maharashtra"),
    ("Nashik", "Maharashtra"),
    ("Nagpur", "Maharashtra"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Delhi", "Delhi"),
    ("Ahmedabad", "Gujarat"),
    ("Chennai", "Tamil Nadu")
]

PRODUCTS = [
    ("Classic Arabica Beans", "Coffee Beans", 499),
    ("Dark Roast Beans", "Coffee Beans", 549),
    ("Medium Roast Beans", "Coffee Beans", 529),
    ("Espresso Blend", "Coffee Beans", 599),
    ("Cold Brew Blend", "Coffee Beans", 649),
    ("Hazelnut Coffee", "Flavoured Coffee", 449),
    ("Vanilla Coffee", "Flavoured Coffee", 449),
    ("Caramel Coffee", "Flavoured Coffee", 469),
    ("Mocha Coffee", "Flavoured Coffee", 489),
    ("French Vanilla", "Flavoured Coffee", 479),
    ("Coffee Mug", "Merchandise", 299),
    ("Travel Mug", "Merchandise", 499),
    ("French Press", "Equipment", 999),
    ("Coffee Dripper", "Equipment", 699),
    ("Coffee Grinder", "Equipment", 1499)
]


# -----------------------------
# Utility functions
# -----------------------------

def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def write_csv(filename, rows, fieldnames):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUT_DIR / filename

    with filepath.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filepath}")


# -----------------------------
# Generate customers
# -----------------------------

def generate_customers():
    customers = []

    start_date = date(2025, 1, 1)
    end_date = date(2026, 9, 1)

    for i in range(1, NUM_CUSTOMERS + 1):

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city, state = random.choice(CITIES)

        customer = {
            "customer_id": f"CUST{i:04d}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
            "city": city,
            "state": state,
            "signup_date": random_date(start_date, end_date)
        }

        customers.append(customer)

    write_csv(
        "customers.csv",
        customers,
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "city",
            "state",
            "signup_date"
        ]
    )


# -----------------------------
# Generate products
# -----------------------------

def generate_products():
    products = []

    for i, (name, category, price) in enumerate(PRODUCTS, start=1):

        product = {
            "product_id": f"PROD{i:03d}",
            "product_name": name,
            "category": category,
            "unit_price": price,
            "stock_quantity": random.randint(10, 500),
            "product_status": random.choice(["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"])
        }

        products.append(product)

    write_csv(
        "products.csv",
        products,
        [
            "product_id",
            "product_name",
            "category",
            "unit_price",
            "stock_quantity",
            "product_status"
        ]
    )

# -----------------------------
# Generate orders and order items
# -----------------------------

def generate_orders_and_items():
    customers = []
    products = []

    # Read customers
    with (OUTPUT_DIR / "customers.csv").open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        customers = list(csv.DictReader(file))

    # Read products
    with (OUTPUT_DIR / "products.csv").open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        products = list(csv.DictReader(file))

    orders = []
    order_items = []

    order_start_date = date(2025, 1, 1)
    order_end_date = date(2026, 9, 30)

    for order_number in range(1, NUM_ORDERS + 1):

        order_id = f"ORD{order_number:05d}"

        customer = random.choice(customers)

        order_date = random_date(
            order_start_date,
            order_end_date
        )

        order_status = random.choices(
            ["COMPLETED", "CANCELLED", "PENDING"],
            weights=[85, 10, 5],
            k=1
        )[0]

        number_of_items = random.randint(1, 4)

        selected_products = random.sample(
            products,
            number_of_items
        )

        order_total = 0

        for item_number, product in enumerate(
            selected_products,
            start=1
        ):

            quantity = random.randint(1, 5)

            unit_price = float(product["unit_price"])

            item_total = quantity * unit_price

            order_total += item_total

            order_item = {
                "order_item_id": f"ITEM{order_number:05d}{item_number:02d}",
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": unit_price
            }

            order_items.append(order_item)

        order = {
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "order_date": order_date,
            "campaign_id": None,
            "order_status": order_status,
            "total_amount": round(order_total, 2)
        }

        orders.append(order)

    write_csv(
        "orders.csv",
        orders,
        [
            "order_id",
            "customer_id",
            "order_date",
            "campaign_id",
            "order_status",
            "total_amount"
        ]
    )

    write_csv(
        "order_items.csv",
        order_items,
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price"
        ]
    )
# -----------------------------
# Generate marketing campaigns
# -----------------------------

def generate_marketing():
    campaigns = []

    campaign_names = [
        "Summer Cold Brew",
        "Monsoon Coffee Fest",
        "Weekend Coffee Sale",
        "New Customer Offer",
        "Diwali Coffee Sale",
        "Winter Warmers",
        "Valentine Coffee Box",
        "Republic Day Sale",
        "Independence Day Sale",
        "Premium Beans Launch",
        "Cold Brew Launch",
        "Coffee Lovers Week",
        "Festive Gift Collection",
        "Mid-Year Sale",
        "Back to Work Coffee",
        "Weekend Flash Sale",
        "New Product Launch",
        "Loyalty Rewards",
        "First Order Offer",
        "Year End Coffee Sale"
    ]

    channels = [
        "Instagram",
        "Google",
        "Email",
        "Facebook"
    ]

    for i, campaign_name in enumerate(
        campaign_names,
        start=1
    ):

        start_date = random_date(
            date(2025, 1, 1),
            date(2026, 8, 1)
        )

        end_date = start_date + timedelta(
            days=random.randint(7, 30)
        )

        campaign = {
            "campaign_id": f"CAM{i:03d}",
            "campaign_name": campaign_name,
            "channel": random.choice(channels),
            "start_date": start_date,
            "end_date": end_date,
            "budget": random.choice([
                10000,
                20000,
                30000,
                50000,
                75000
            ]),
            "conversions": random.randint(20, 500)
        }

        campaigns.append(campaign)

    write_csv(
        "marketing.csv",
        campaigns,
        [
            "campaign_id",
            "campaign_name",
            "channel",
            "start_date",
            "end_date",
            "budget",
            "conversions"
        ]
    )


# -----------------------------
# Generate payments
# -----------------------------

def generate_payments():
    orders = []

    with (OUTPUT_DIR / "orders.csv").open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        orders = list(csv.DictReader(file))

    payments = []

    payment_methods = [
        "UPI",
        "CARD",
        "COD",
        "NET_BANKING"
    ]

    for i, order in enumerate(orders, start=1):

        status = random.choices(
            ["SUCCESS", "FAILED", "REFUNDED"],
            weights=[90, 7, 3],
            k=1
        )[0]

        payment = {
            "payment_id": f"PAY{i:05d}",
            "order_id": order["order_id"],
            "payment_date": order["order_date"],
            "payment_method": random.choice(
                payment_methods
            ),
            "payment_status": status,
            "amount": float(order["total_amount"])
        }

        payments.append(payment)

    write_csv(
        "payments.csv",
        payments,
        [
            "payment_id",
            "order_id",
            "payment_date",
            "payment_method",
            "payment_status",
            "amount"
        ]
    )

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    generate_customers()
    generate_products()
    generate_orders_and_items()
    generate_marketing()
    generate_payments()

    print("\nSource data generation completed.")