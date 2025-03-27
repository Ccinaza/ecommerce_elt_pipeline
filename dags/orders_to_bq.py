from datetime import datetime
from airflow.models import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import os

# Configuration variables
SOURCE_TABLE_NAME = 'orders'
SOURCE_SCHEMA = 'public'
# Define GCP variables
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GCP_BUCKET = os.getenv('GCP_BUCKET_NAME')
BQ_DATASET = os.getenv('BIGQUERY_DATASET', 'ecommerce')
execution_date = "{{ ds_nodash }}"
GCS_KEY = f'postgres_{SOURCE_SCHEMA}/{SOURCE_TABLE_NAME}/{execution_date}.json'
POSTGRES_CONN = 'postgres_default'
GCP_CONN = 'google_cloud_default'


default_args = {
    'owner': 'Blessing Angus',
}

dag = DAG(
    dag_id=f'load_{SOURCE_TABLE_NAME}_postgres_to_bq',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 3, 27),
    catchup=False,
    tags=['postgres', 'bigquery', 'full_load'],
)

# Extract data from PostgreSQL to GCS
postgres_to_gcs = PostgresToGCSOperator(
    task_id='postgres_to_gcs',
    postgres_conn_id=POSTGRES_CONN,
    sql=f"SELECT * FROM {SOURCE_SCHEMA}.{SOURCE_TABLE_NAME};",
    bucket=GCP_BUCKET,
    filename=GCS_KEY,
    export_format='NEWLINE_DELIMITED_JSON',
    gcp_conn_id=GCP_CONN,
    dag=dag,
)

# Load data from GCS to BigQuery (Autodetect schema & create table if missing)
load_gcs_to_bq = GCSToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket=GCP_BUCKET,
    source_objects=[GCS_KEY],
    destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{SOURCE_TABLE_NAME}',
    source_format='NEWLINE_DELIMITED_JSON',
    write_disposition='WRITE_TRUNCATE',  # Overwrite existing data (change if needed)
    create_disposition='CREATE_IF_NEEDED',  # Creates table if missing
    autodetect=True,  # Infer schema automatically
    gcp_conn_id=GCP_CONN,
    dag=dag,
)

postgres_to_gcs >> load_gcs_to_bq