from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import os

# Define default arguments for the DAG
default_args = {
    'owner': 'Blessing',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'postgres_data_ingestion',
    default_args=default_args,
    description='Load CSV data into PostgreSQL',
    schedule_interval=None,  # Set to None for manual triggers or use a cron expression
    catchup=False
)

# Mapping tables to their csv files - Update this with the path inside the container
csv_paths = {
    'customers': '/opt/airflow/data/olist_customers_dataset.csv',
    'geolocation': '/opt/airflow/data/olist_geolocation_dataset.csv',
    'order_items': '/opt/airflow/data/olist_order_items_dataset.csv',
    'order_payments': '/opt/airflow/data/olist_order_payments_dataset.csv',
    'order_reviews': '/opt/airflow/data/olist_order_reviews_dataset.csv',
    'orders': '/opt/airflow/data/olist_orders_dataset.csv',
    'products': '/opt/airflow/data/olist_products_dataset.csv',
    'sellers': '/opt/airflow/data/olist_sellers_dataset.csv',
    'product_category_name_translation': '/opt/airflow/data/product_category_name_translation.csv',
}

def ingest_table_data(table_name, csv_path, **kwargs):
    """
    Function to ingest data from CSV into PostgreSQL
    """
    # Get database connection parameters from environment variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        print(f"Ingesting data into the '{table_name}' table...")
        
        # Load data into PostgreSQL
        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, if_exists='replace', index=False, chunksize=1000)
        
        print(f"Data successfully ingested into the '{table_name}' table.")
        return f"Successfully ingested {table_name}"
    
    except Exception as e:
        print(f"Error ingesting data into the '{table_name}' table: {e}")
        raise e

# Create a task for each table
for table, path in csv_paths.items():
    task = PythonOperator(
        task_id=f'ingest_{table}_data',
        python_callable=ingest_table_data,
        op_kwargs={'table_name': table, 'csv_path': path},
        dag=dag,
    )