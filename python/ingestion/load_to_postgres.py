import csv
import psycopg2
from pathlib import Path

DB_NAME = "magic_roast"
DB_USER = "shivam"
DB_HOST = "localhost"
DB_PORT = "5432"

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "marketing": "marketing.csv",
}


def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )


def load_table(cursor, table_name, file_name):
    file_path = RAW_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        columns = next(reader)

        rows = list(reader)

    placeholders = ", ".join(["%s"] * len(columns))
    column_list = ", ".join(columns)

    query = f"""
        INSERT INTO raw.{table_name} ({column_list})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING;
    """

    cursor.executemany(query, rows)

    print(f"{table_name}: {len(rows)} rows processed")


def main():
    conn = connect_db()

    try:
        with conn:
            with conn.cursor() as cursor:

                for table_name, file_name in FILES.items():
                    load_table(cursor, table_name, file_name)

        print("\nPipeline completed successfully.")

    except Exception as e:
        print(f"\nPipeline failed: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()