'''First python Script'''

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level=logging.DEBUG, #Records all log messages from DEBUG level and above.
    format ="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a" # filemode = append 
)
engine = create_engine('sqlite:///inventory.db') 
'''inventory.db is the name of database'''
def ingest_db(df , table_name , engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con =engine, if_exists = 'replace' , index = False)
    #saves df as a sql table named table_name , connected by engine, replacing the table if it already exists and without storing the dataframe index
def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('data/data'):
        if file.endswith(".csv"): 
            df = pd.read_csv(os.path.join("data" , "data",file))
            #os.path.join() automatically creates the correct path for your operating system
            logging.info(f'ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info("Ingestion Complete ")
    logging.info(f'Total time taken:{total_time} minutes')

if __name__ =='__main__':
    load_raw_data()
    #This ensures load_raw_data() runs only when the script is executed directly, not when it is imported into another Python file.  