import psycopg2

DB_NAME = "magic_roast"
DB_USER = "shivam"
DB_HOST = "localhost"
DB_PORT = "5432"


def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )


def run_transformations(cursor):

    # -------------------------
    # STAGING
    # -------------------------

    staging_sql = """

    DROP TABLE IF EXISTS staging.customers CASCADE;
    CREATE TABLE staging.customers AS
    SELECT
        TRIM(customer_id) AS customer_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        LOWER(TRIM(email)) AS email,
        TRIM(city) AS city,
        TRIM(state) AS state,
        signup_date
    FROM raw.customers;


    DROP TABLE IF EXISTS staging.products CASCADE;
    CREATE TABLE staging.products AS
    SELECT
        TRIM(product_id) AS product_id,
        TRIM(product_name) AS product_name,
        TRIM(category) AS category,
        unit_price,
        stock_quantity,
        UPPER(TRIM(product_status)) AS product_status
    FROM raw.products;


    DROP TABLE IF EXISTS staging.orders CASCADE;
    CREATE TABLE staging.orders AS
    SELECT
        TRIM(order_id) AS order_id,
        TRIM(customer_id) AS customer_id,
        order_date,
        TRIM(campaign_id) AS campaign_id,
        UPPER(TRIM(order_status)) AS order_status,
        total_amount
    FROM raw.orders;


    DROP TABLE IF EXISTS staging.order_items CASCADE;
    CREATE TABLE staging.order_items AS
    SELECT
        TRIM(order_item_id) AS order_item_id,
        TRIM(order_id) AS order_id,
        TRIM(product_id) AS product_id,
        quantity,
        unit_price
    FROM raw.order_items;


    DROP TABLE IF EXISTS staging.payments CASCADE;
    CREATE TABLE staging.payments AS
    SELECT
        TRIM(payment_id) AS payment_id,
        TRIM(order_id) AS order_id,
        payment_date,
        UPPER(TRIM(payment_method)) AS payment_method,
        UPPER(TRIM(payment_status)) AS payment_status,
        amount
    FROM raw.payments;


    DROP TABLE IF EXISTS staging.marketing CASCADE;
    CREATE TABLE staging.marketing AS
    SELECT
        TRIM(campaign_id) AS campaign_id,
        TRIM(campaign_name) AS campaign_name,
        TRIM(channel) AS channel,
        start_date,
        end_date,
        budget,
        conversions
    FROM raw.marketing;

    """

    cursor.execute(staging_sql)

    # -------------------------
    # ANALYTICS
    # -------------------------

    analytics_sql = """

    DROP TABLE IF EXISTS analytics.fact_order_items CASCADE;
    DROP TABLE IF EXISTS analytics.fact_orders CASCADE;
    DROP TABLE IF EXISTS analytics.dim_customer CASCADE;
    DROP TABLE IF EXISTS analytics.dim_product CASCADE;
    DROP TABLE IF EXISTS analytics.dim_marketing CASCADE;
    DROP TABLE IF EXISTS analytics.dim_date CASCADE;


    CREATE TABLE analytics.dim_customer AS
    SELECT *
    FROM staging.customers;


    CREATE TABLE analytics.dim_product AS
    SELECT *
    FROM staging.products;


    CREATE TABLE analytics.dim_marketing AS
    SELECT *
    FROM staging.marketing;


    CREATE TABLE analytics.dim_date AS
    SELECT DISTINCT
        order_date AS date_key,
        EXTRACT(YEAR FROM order_date)::INT AS year,
        EXTRACT(MONTH FROM order_date)::INT AS month,
        EXTRACT(DAY FROM order_date)::INT AS day,
        EXTRACT(QUARTER FROM order_date)::INT AS quarter,
        TO_CHAR(order_date, 'Month') AS month_name,
        TO_CHAR(order_date, 'Day') AS day_name
    FROM staging.orders;


    CREATE TABLE analytics.fact_orders AS
    SELECT
        o.order_id,
        o.customer_id,
        o.campaign_id,
        o.order_date AS date_key,
        o.order_status,
        o.total_amount AS order_value,
        COALESCE(
            SUM(
                CASE
                    WHEN p.payment_status = 'SUCCESS'
                    THEN p.amount
                    ELSE 0
                END
            ),
            0
        ) AS realized_revenue
    FROM staging.orders o
    LEFT JOIN staging.payments p
        ON o.order_id = p.order_id
    GROUP BY
        o.order_id,
        o.customer_id,
        o.campaign_id,
        o.order_date,
        o.order_status,
        o.total_amount;


    CREATE TABLE analytics.fact_order_items AS
    SELECT
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        o.customer_id,
        o.order_date AS date_key,
        oi.quantity,
        oi.unit_price,
        (oi.quantity * oi.unit_price)::NUMERIC(12,2) AS line_amount
    FROM staging.order_items oi
    JOIN staging.orders o
        ON oi.order_id = o.order_id;

    """

    cursor.execute(analytics_sql)


def main():

    conn = connect_db()

    try:
        with conn:
            with conn.cursor() as cursor:
                run_transformations(cursor)

        print("Transformations completed successfully.")

    except Exception as e:
        print(f"Transformation failed: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()