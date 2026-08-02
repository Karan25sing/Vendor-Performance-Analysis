'''First python Script'''

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time


#Ensure the logs directory exists before setting up logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level=logging.DEBUG, #Records all log messages from DEBUG level and above.
    format ="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a" # filemode = append 
)
# --- POSTGRESQL CONNECTION CONFIGURATION ---

DB_USER = "postgres"
DB_PASSWORD = "Cgc23%404165"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "inventory"  

# PostgreSQL connection string using psycopg2 driver
connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(connection_string) 

'''inventory is the name of database'''
def ingest_db(df, table_name, engine):
    """Ingests a DataFrame into a PostgreSQL database table efficiently."""
    # Convert column names to lowercase to avoid PostgreSQL quote-sensitivity issues
    df.columns = [col.strip().lower() for col in df.columns]

    df.to_sql(
        name=table_name.lower(),
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=10000,  # Inserts in batches to optimize speed/memory usage for large CSVs
        method="multi",  # Speeds up bulk inserts into PostgreSQL
    )


def load_raw_data():
    """Loads CSV files from the data directory and ingests them into PostgreSQL."""
    start = time.time()
    data_dir = os.path.join("data", "data")

    if not os.path.exists(data_dir):
        logging.error(f"Directory {data_dir} does not exist!")
        print(f"Error: Path {data_dir} not found.")
        return

    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(data_dir, file)
            table_name = file[:-4]  # Strip '.csv' from filename

            logging.info(f"Ingesting {file} into database table: {table_name}")
            print(f"Ingesting {file}...")

            df = pd.read_csv(file_path)
            ingest_db(df, table_name, engine)

    end = time.time()
    total_time = (end - start) / 60
    logging.info("Ingestion Complete")
    logging.info(f"Total time taken: {total_time:.2f} minutes")
    print(
        f"Ingestion Complete! Total time taken: {total_time:.2f} minutes"
    )


if __name__ == "__main__":
    load_raw_data()