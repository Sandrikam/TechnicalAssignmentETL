import requests
import psycopg2
from db_config import DB_CONFIG
from datetime import datetime

# --- API CONFIG
NBG_API_URL = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date=2025-05-23"

# --- DB CONFIG
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "PrimeDB",
    "user": "admin",
    "password": "admin"
}

# --- Fetch exchange rates
def fetch_exchange_rates():
    response = requests.get(NBG_API_URL)
    response.raise_for_status()
    data = response.json()
    return data[0]["currencies"], data[0]["date"]

# --- Insert into dim_currency
def insert_into_db(currencies, rate_date):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for item in currencies:
        code = item["code"]
        rate = float(item["rate"])
        cursor.execute("""
            INSERT INTO dim_currency (currency_code, rate_to_usd, rate_date)
            VALUES (%s, %s, %s)
            ON CONFLICT (currency_code, rate_date) DO NOTHING
        """, (code, rate, rate_date))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(currencies)} exchange rates for {rate_date}")

# --- MAIN ---
if __name__ == "__main__":
    try:
        currencies, rate_date = fetch_exchange_rates()
        insert_into_db(currencies, rate_date)
    except Exception as e:
        print(f"err: {e}")
