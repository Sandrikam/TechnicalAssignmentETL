import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db_config import DB_CONFIG
from getMonthlySalesSummary import get_monthly_sales_summary
from getSalesAffiliateCategory import get_sales_by_affiliate_category
from getSalesWithOriginalAmount import get_sales_with_original_amount

engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)
os.makedirs("reports", exist_ok=True)

def generate_sales_chart(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['month'].astype(str) + '/' + df['year'].astype(str), df['total_sales_usd'], marker='o', color='teal')
    plt.title("Monthly Sales Trend", fontsize=14)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Total Sales (USD)", fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/sales_trend.png")
    plt.close()

def generate_pdf_report(monthly_df, affiliate_df):
    doc = SimpleDocTemplate("reports/monthly_report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Monthly Sales Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Records: {len(monthly_df)}", styles['Normal']))
    elements.append(Paragraph(f"Total Sales: ${monthly_df['total_sales_usd'].sum():,.2f}", styles['Normal']))
    elements.append(Paragraph(f"Avg Transaction: ${monthly_df['avg_transaction_usd'].mean():,.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))

    monthly_data = [['Year', 'Month', 'Total Sales (USD)', 'Transactions', 'Avg Transaction']]
    for row in monthly_df.itertuples():
        monthly_data.append([
            row.year, row.month,
            f"${row.total_sales_usd:,.2f}",
            row.num_transactions,
            f"${row.avg_transaction_usd:,.2f}"
        ])
    table = Table(monthly_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    elements.append(Image("reports/sales_trend.png", width=450, height=200))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Sales by Affiliate and Category", styles['Heading2']))
    affiliate_data = [['Affiliate', 'Category', 'Total Sales (USD)']]
    for row in affiliate_df.itertuples():
        affiliate_data.append([row.affiliate or '-', row.category or '-', f"${row.total_sales_usd:,.2f}"])

    table2 = Table(affiliate_data)
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#445")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table2)

    doc.build(elements)

def generate_full_report():
    monthly = get_monthly_sales_summary()
    affiliate = get_sales_by_affiliate_category()
    _ = get_sales_with_original_amount()
    generate_sales_chart(monthly)
    generate_pdf_report(monthly, affiliate)

if __name__ == "__main__":
    generate_full_report()
