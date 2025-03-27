import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Create engine using the engine object directly
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


# Defining base path for CSV files
BASE_PATH = '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/ecommerce_elt_pipeline/data'

# Mapping tables to their csv files
csv_paths = {
    'customers': f'{BASE_PATH}/olist_customers_dataset.csv',
    'geolocation': f'{BASE_PATH}/olist_geolocation_dataset.csv',
    'order_items': f'{BASE_PATH}/olist_order_items_dataset.csv',
    'order_payments': f'{BASE_PATH}/olist_order_payments_dataset.csv',
    'order_reviews': f'{BASE_PATH}/olist_order_reviews_dataset.csv',
    'orders': f'{BASE_PATH}/olist_orders_dataset.csv',
    'products': f'{BASE_PATH}/olist_products_dataset.csv',
    'sellers': f'{BASE_PATH}/olist_sellers_dataset.csv',
    'product_category_name_translation': f'{BASE_PATH}/product_category_name_translation.csv',
}

def ingest_data():
     for table, path in csv_paths.items():
          try:
            df = pd.read_csv(path)
            print(f"Ingesting data into the '{table}' table...")
        
            # Add chunk_size for handling large datasets
            with engine.connect() as connection: #allows pandas to recognize the SQLAlchemy Engine as a valid “connectable” 
                df.to_sql(table, con=connection, if_exists='replace', index=False, chunksize=1000)
                print(f"Data successfully ingested into the '{table}' table.")

          except Exception as e:
            print(f"Error ingesting data into the '{table}' table: {e}")

if __name__ == "__main__":
    ingest_data()