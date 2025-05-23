import pandas as pd
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

def get_sales_by_affiliate_category():
    query = """
    SELECT
        da.name AS affiliate,
        dc.name AS category,
        SUM(fs.amount_usd) AS total_sales_usd
    FROM fact_sales fs
    LEFT JOIN dim_affiliate da ON fs.affiliate_id = da.id
    LEFT JOIN dim_category dc ON fs.category_id = dc.id
    GROUP BY da.name, dc.name
    ORDER BY total_sales_usd DESC;
    """
    df = pd.read_sql(query, engine)
    df.to_csv("reports/sales_by_affiliate_category.csv", index=False)
    return df