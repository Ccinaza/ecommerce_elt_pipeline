from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import os

# Configuration variables
SOURCE_TABLE_NAME = 'geolocation'
SOURCE_SCHEMA = 'public'
BATCH_SIZE = 50000  # Number of rows per batch
MAX_ROWS = 1000165  # Estimated total rows (adjust accordingly)
NUM_BATCHES = MAX_ROWS // BATCH_SIZE  # Total batch count

# Define GCP variables
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GCP_BUCKET = os.getenv('GCP_BUCKET_NAME')
BQ_DATASET = os.getenv('BIGQUERY_DATASET', 'ecommerce')
POSTGRES_CONN = 'postgres_default'
GCP_CONN = 'google_cloud_default'

default_args = {
    'owner': 'Blessing Angus',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 27),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id=f'load_{SOURCE_TABLE_NAME}_postgres_to_bq',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['postgres', 'bigquery', 'batch_load'],
)

# Dynamically create batch extraction tasks
extract_tasks = []
gcs_objects = []

for batch_num in range(NUM_BATCHES):
    batch_offset = batch_num * BATCH_SIZE
    execution_date = "{{ ds_nodash }}"  # Keeps execution date consistent

    # Unique GCS file per batch
    gcs_key = f'postgres_{SOURCE_SCHEMA}/{SOURCE_TABLE_NAME}/batch_{batch_num}_{execution_date}.json'
    gcs_objects.append(gcs_key)  # Collect for BigQuery load

    extract_task = PostgresToGCSOperator(
        task_id=f'postgres_to_gcs_batch_{batch_num}',
        postgres_conn_id=POSTGRES_CONN,
        sql=f"SELECT * FROM {SOURCE_SCHEMA}.{SOURCE_TABLE_NAME} LIMIT {BATCH_SIZE} OFFSET {batch_offset};",
        bucket=GCP_BUCKET,
        filename=gcs_key,
        export_format='NEWLINE_DELIMITED_JSON',
        gcp_conn_id=GCP_CONN,
        dag=dag,
    )

    extract_tasks.append(extract_task)

# Load all batch files from GCS to BigQuery
load_gcs_to_bq = GCSToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket=GCP_BUCKET,
    source_objects=gcs_objects,  # Load all batch files at once
    destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{SOURCE_TABLE_NAME}',
    source_format='NEWLINE_DELIMITED_JSON',
    write_disposition='WRITE_APPEND',  # Append instead of overwrite
    create_disposition='CREATE_IF_NEEDED',
    autodetect=True,
    gcp_conn_id=GCP_CONN,
    dag=dag,
)

# Set task dependencies (all extract tasks >> load to BQ)
extract_tasks >> load_gcs_to_bq
