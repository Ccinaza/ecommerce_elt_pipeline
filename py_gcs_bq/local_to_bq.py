from gcp_manager import BigQueryManager
from bq_config import (
    PROJECT_ID, 
    DATASET_ID, 
    TABLE_CONFIGS, 
    DATA_PATH
)
import os

def load_to_bigquery():
    # Initialize BigQuery client
    bq_manager = BigQueryManager(project_id=PROJECT_ID)
    
    # Create dataset
    bq_manager.create_dataset(dataset_id=DATASET_ID)
    
    # Load each table
    for table_id, config in TABLE_CONFIGS.items():
        file_path = os.path.join(DATA_PATH, config['file_name'])
        
        # Create and load table
        bq_manager.create_table(
            dataset_id=DATASET_ID,
            table_id=table_id,
            schema=config['schema']
        )
        
        bq_manager.load_from_local(
            dataset_id=DATASET_ID,
            table_id=table_id,
            source_file=file_path,
            file_format='csv',
            schema=config['schema'],
            field_delimiter=';'
        )

if __name__ == "__main__":
    load_to_bigquery()
