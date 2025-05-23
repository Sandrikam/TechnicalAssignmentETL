import pandas as pd
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

def get_sales_with_original_amount():
    query = """
    SELECT
        fs.sale_id,
        dc.currency_code,
        dc.rate_to_usd,
        fs.amount_usd,
        ROUND(fs.amount_usd * dc.rate_to_usd, 2) AS original_amount
    FROM fact_sales fs
    JOIN dim_currency dc ON fs.currency_id = dc.id;
    """
    df = pd.read_sql(query, engine)
    df.to_csv("reports/sales_original_amount.csv", index=False)
    return df