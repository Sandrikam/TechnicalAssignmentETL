import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db_config import DB_CONFIG

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

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
ORDER BY dd.year, dd.month
"""

df = pd.read_sql(query, engine)

df.to_csv("reports/monthly_sales_summary.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(df['month'].astype(str) + '/' + df['year'].astype(str), df['total_sales_usd'], marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/sales_trend.png")
plt.close()
