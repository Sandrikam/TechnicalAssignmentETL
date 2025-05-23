import pandas as pd
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

def get_monthly_sales_summary():
    query = """
    SELECT
        dd.year,
        dd.month,
        SUM(fs.amount_usd) AS total_sales_usd,
        COUNT(fs.id) AS num_transactions,
        ROUND(AVG(fs.amount_usd), 2) AS avg_transaction_usd
    FROM fact_sales fs
    JOIN dim_date dd ON fs.date_id = dd.id
    GROUP BY dd.year, dd.month
    ORDER BY dd.year, dd.month;
    """
    df = pd.read_sql(query, engine)
    df.to_csv("reports/monthly_sales_summary.csv", index=False)
    return df