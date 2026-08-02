import os
import logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from ingestion import ingest_db

# ===========================
# LOGGING CONFIGURATION
# ===========================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/get_vendor_sales_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

# ===========================
# POSTGRESQL CONFIGURATION
# ===========================
DB_USER = "postgres"
DB_PASSWORD = "Cgc23%404165"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "inventory"

connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)


def create_vendor_summary(engine):
    """
    Creates the Vendor Sales Summary table from PostgreSQL.
    """

    query = """
    WITH freightsummary AS (
        SELECT
            vendor_number,
            SUM(freight) AS totalfreightcost
        FROM vendor_invoice
        GROUP BY vendor_number
    ),

    purchasesummary AS (
        SELECT
            p.vendor_number,
            p.vendor_name,
            p.brand,
            p.description,
            p.purchaseprice,
            pp.price AS actualprice,
            pp.volume,

            SUM(p.quality) AS totalpurchasequantity,
            SUM(p.dollars) AS totalpurchasedollars

        FROM purchase p

        JOIN purchase_prices pp
            ON p.brand = pp.brand
            AND p.description = pp.description

        WHERE p.purchaseprice > 0

        GROUP BY
            p.vendor_number,
            p.vendor_name,
            p.brand,
            p.description,
            p.purchaseprice,
            pp.price,
            pp.volume
    ),

    salessummary AS (

        SELECT
            vendor_no,
            brand,

            SUM(sales_price) AS totalsalesprice,
            SUM(sales_dollars) AS totalsalesdollars,
            SUM(sales_quantity) AS totalsalesquantity,
            SUM(excise_tax) AS totalexcisetax

        FROM sales

        GROUP BY
            vendor_no,
            brand
    )

    SELECT

        ps.vendor_number AS vendor_number,
        ps.vendor_name AS vendor_name,
        ps.brand,
        ps.description,
        ps.purchaseprice,
        ps.actualprice,
        ps.volume,

        ps.totalpurchasequantity,
        ps.totalpurchasedollars,

        COALESCE(ss.totalsalesprice,0) AS totalsalesprice,
        COALESCE(ss.totalsalesdollars,0) AS totalsalesdollars,
        COALESCE(ss.totalsalesquantity,0) AS totalsalesquantity,
        COALESCE(ss.totalexcisetax,0) AS totalexcisetax,

        COALESCE(fs.totalfreightcost,0) AS totalfreightcost

    FROM purchasesummary ps

    LEFT JOIN salessummary ss
        ON ps.vendor_number = ss.vendor_no
       AND ps.brand = ss.brand

    LEFT JOIN freightsummary fs
        ON ps.vendor_number = fs.vendor_number

    ORDER BY ps.totalpurchasedollars DESC;
    """

    return pd.read_sql_query(query, con=engine)


def clean_data(df):
    """
    Clean data and calculate business KPIs.
    """

    # -------------------------
    # Convert numeric columns
    # -------------------------
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)

    numeric_columns = [
        "totalsalesprice",
        "totalsalesdollars",
        "totalsalesquantity",
        "totalexcisetax",
        "totalfreightcost",
        "totalpurchasequantity",
        "totalpurchasedollars",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # -------------------------
    # Remove NULLs
    # -------------------------
    df.fillna(0, inplace=True)

    # -------------------------
    # Clean text columns
    # -------------------------
    if "vendor_name" in df.columns:
        df["vendor_name"] = df["vendor_name"].astype(str).str.strip()

    if "description" in df.columns:
        df["description"] = df["description"].astype(str).str.strip()

    # -------------------------
    # Business Metrics
    # -------------------------
    df["grossprofit"] = (
        df["totalsalesdollars"]
        - df["totalpurchasedollars"]
    )

    df["profitmargin"] = (
        df["grossprofit"] /
        df["totalsalesdollars"] * 100
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    df["stockturnover"] = (
        df["totalsalesquantity"] /
        df["totalpurchasequantity"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    df["salespurchaseratio"] = (
        df["totalsalesdollars"] /
        df["totalpurchasedollars"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    return df


if __name__ == "__main__":

    logging.info("Creating Vendor Sales Summary...")

    print("Executing SQL query...")
    summary_df = create_vendor_summary(engine)

    print("Cleaning data...")
    clean_df = clean_data(summary_df)

    print("\nRows:", clean_df.shape[0])
    print("Columns:", clean_df.shape[1])

    print("\nColumns:")
    print(clean_df.columns.tolist())

    print("\nFirst 5 rows:")
    print(clean_df.head())

    logging.info("Writing vendor_sales_summary to PostgreSQL...")

    ingest_db(clean_df, "vendor_sales_summary", engine)

    logging.info("Completed Successfully.")

    print("\n vendor_sales_summary created successfully!")