from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import os

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'retry_exponential_backoff': True,
}

# GCP Configuration
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GCP_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')
BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET', 'ecommerce')

# PostgreSQL Connection
POSTGRES_CONN_ID = 'postgres_default'

# List of tables to transfer
tables = [
    'customers',
    'geolocation',
    'order_items',
    'order_payments',
    'order_reviews',
    'orders',
    'products',
    'sellers',
    'product_category_name_translation',
]

# Define DAG
with DAG(
    'transfer_to_bq',
    default_args=default_args,
    description='Optimized DAG for PostgreSQL to BigQuery transfer',
    schedule_interval=None,  # Adjust if scheduling is required
    catchup=False,
    max_active_runs=1,  # Prevent overlapping DAG runs
) as dag:

    # Create BigQuery dataset if it doesn’t exist
    create_dataset_task = BigQueryCreateEmptyDatasetOperator(
        task_id='create_bigquery_dataset',
        dataset_id=BIGQUERY_DATASET,
        project_id=GCP_PROJECT_ID,
        exists_ok=True,
    )

    # Group tasks for parallel execution
    with TaskGroup(group_id="transfer_tasks") as transfer_tasks:
        for table in tables:
            # Export PostgreSQL table to GCS
            export_task = PostgresToGCSOperator(
                task_id=f'export_{table}_to_gcs',
                postgres_conn_id=POSTGRES_CONN_ID,
                sql=f'SELECT * FROM {table}',
                bucket=GCP_BUCKET_NAME,
                filename=f'data/{table}/{table}_{{{{ ds }}}}.json',  # Organized by date
                export_format='json',
                retries=3,
            )

            # Load data from GCS to BigQuery
            load_task = GCSToBigQueryOperator(
                task_id=f'load_{table}_to_bigquery',
                bucket=GCP_BUCKET_NAME,
                source_objects=[f'data/{table}/{table}_{{{{ ds }}}}.json'],
                destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table}',
                write_disposition='WRITE_APPEND',  # Append instead of overwrite
                source_format='NEWLINE_DELIMITED_JSON',
                autodetect=True,
                retries=1,
                timeout=300
            )

            # Task dependencies
            export_task >> load_task

    # DAG flow
    create_dataset_task >> transfer_tasks
