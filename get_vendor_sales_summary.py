import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db

logging.basicConfig(
    filename= "logs/get_vendor_sales_summary.log",
    level=logging.DEBUG,
    format ="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)
def create_vendor_summary(conn):
    '''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""With FreightSummary AS(Select  VendorNumber, SUM(Freight) as TotalFreightCost
                                    
                                    From vendor_invoice  
                                    Group BY VendorNumber ),
                                         
PurchaseSummary AS (
 Select  p.VendorNumber, p.VendorName, p.Brand,p.Description, p.PurchasePrice,
pp.Price as ActualPrice, pp.volume,
SUM(Quantity) as TotalPurchaseQuantity,
Sum(Dollars) as TotalPurchaseDollars     
FROM purchases p
JOIN purchase_prices pp
    On p.Brand = pp.Brand
Where p.PurchasePrice > 0
GROUP BY p.VendorNumber , p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume),

SalesSummary AS( Select VendorNo,Brand,SUM(SalesPrice) as TotalSalesprice,
                  SUM(SalesDollars) as TotalSalesDollars,
                  SUM(SalesQuantity) as TotalSalesQuantity,
                  SUM(ExciseTax) as TotalExciseTax
        FROM sales
        Group By VendorNo, Brand
)
                                         
Select ps.VendorNumber, ps.VendorName, ps.Brand,ps.Description, ps.PurchasePrice,
ps.ActualPrice, ps.Volume, ps.TotalPurchaseQuantity,ps.TotalPurchaseDollars,
ss.TotalSalesprice, ss.TotalSalesDollars, ss.TotalSalesQuantity, ss.TotalExciseTax,fs.TotalFreightCost
From PurchaseSummary ps
Left join SalesSummary ss
 ON ps.VendorNumber = ss.VendorNo
 AND ps.Brand = ss.Brand
Left Join FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
Order BY ps.totalPurchaseDollars DESC""", conn)
    return vendor_sales_summary

def clean_data(df):
    '''this function will clean the data'''
    # changing datatype to float
    df['volume'] = df['volume'].astype('float')

    #filling missing value with 0
    df.fillna(0, inplace = True)
    
    # removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollars'])*100
    df['stockturnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity'] 
    df['SalesPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    # creating database connection
    conn = sqlite3.connect('inventory.db')
    logging.info('Creating Vendor Summary table....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data.....')
    ingest_db(clean_df, 'vendor_sales_summary',conn)
    logging.info('Completed')