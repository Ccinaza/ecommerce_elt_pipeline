from schemas.ecommerce_schema import (
    CUSTOMER_SCHEMA,
    ORDERS_SCHEMA,
    PRODUCTS_SCHEMA,
    SELLERS_SCHEMA,
    ORDER_ITEMS_SCHEMA,
    ORDER_PAYMENTS_SCHEMA,
    ORDER_REVIEWS_SCHEMA,
    GEOLOCATION_SCHEMA,
    PRODUCT_CATEGORY_TRANSLATION_SCHEMA
)

PROJECT_ID = "smiling-audio-448313-p0"
DATASET_ID = "ecommerce"
LOCATION = "europe-west1"
BUCKET_NAME="alt-ecommerce-data"

# Data Mappings
TABLE_CONFIGS = {
    'customers': {
        'schema': CUSTOMER_SCHEMA,
        'file_name': 'olist_customers_dataset.csv'
    },
    'orders': {
        'schema': ORDERS_SCHEMA,
        'file_name': 'olist_orders_dataset.csv'
    },
    'products': {
        'schema': PRODUCTS_SCHEMA,
        'file_name': 'olist_products_dataset.csv'
    },
    'sellers': {
        'schema': SELLERS_SCHEMA,
        'file_name': 'olist_sellers_dataset.csv'
    },
    'order_items': {
        'schema': ORDER_ITEMS_SCHEMA,
        'file_name': 'olist_order_items_dataset.csv'
    },
    'order_payments': {
        'schema': ORDER_PAYMENTS_SCHEMA,
        'file_name': 'olist_order_payments_dataset.csv'
    },
    'order_reviews': {
        'schema': ORDER_REVIEWS_SCHEMA,
        'file_name': 'olist_order_reviews_dataset.csv'
    },
    'geolocation': {
        'schema': GEOLOCATION_SCHEMA,
        'file_name': 'olist_geolocation_dataset.csv'
    },
    'product_category_translation': {
        'schema': PRODUCT_CATEGORY_TRANSLATION_SCHEMA,
        'file_name': 'product_category_translation.csv'
    }
}

# Base Paths
BASE_PATH = '/Users/blessingangus/Downloads/data_engineering/personal_de_projects/E-commerce Capstone'
DATA_PATH = f"{BASE_PATH}/e-commerce_datasets"
SCHEMA_PATH = f"{BASE_PATH}/ecommerce_elt_pipeline/py_gcs_bq/schemas/ecommerce_schema.py"