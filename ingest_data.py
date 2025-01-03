import pandas as pd
from sqlalchemy import create_engine

# creating connection
DB_NAME = 'ecommerce'
DB_USER = 'naza'
DB_PASSWORD = 'veedez_2024'
DB_HOST = 'localhost'
DB_PORT = '5433'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Mapping tables to their csv paths
csv_paths = {
    'customers': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_customers_dataset.csv',
    'geolocation': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_geolocation_dataset.csv',
    'order_items': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_order_items_dataset.csv',
    'order_payments': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_order_payments_dataset.csv',
    'order_reviews': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_order_reviews_dataset.csv',
    'orders': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_orders_dataset.csv',
    'products': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_products_dataset.csv',
    'sellers': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/olist_sellers_dataset.csv',
    'product_category_name_translation': '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone/E-commerce Dataset/product_category_name_translation.csv',
}

# loop through the csv paths and load data into the database
for table, path in csv_paths.items():
    try:
        df = pd.read_csv(path)
        print(f"Ingesting data into the '{table}' table...")

        df.to_sql(table, engine, if_exists='replace', index=False)
        print(f"Data successfully ingested into the '{table}' table.")
    
    except Exception as e:
        print(f"Error ingesting data into the '{table}' table: {e}")