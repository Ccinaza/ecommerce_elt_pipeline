from google.cloud import bigquery

# Table Schemas for Brazilian E-commerce Dataset
CUSTOMER_SCHEMA = [
    bigquery.SchemaField("customer_id", "STRING"),
    bigquery.SchemaField("customer_unique_id", "STRING"),
    bigquery.SchemaField("customer_zip_code_prefix", "STRING"),
    bigquery.SchemaField("customer_city", "STRING"),
    bigquery.SchemaField("customer_state", "STRING")
]

GEOLOCATION_SCHEMA = [
    bigquery.SchemaField("geolocation_zip_code_prefix", "STRING"),
    bigquery.SchemaField("geolocation_lat", "FLOAT"),
    bigquery.SchemaField("geolocation_lng", "FLOAT"),
    bigquery.SchemaField("geolocation_city", "STRING"),
    bigquery.SchemaField("geolocation_state", "STRING")
]

ORDER_ITEMS_SCHEMA = [
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("order_item_id", "INTEGER"),
    bigquery.SchemaField("product_id", "STRING"),
    bigquery.SchemaField("seller_id", "STRING"),
    bigquery.SchemaField("shipping_limit_date", "TIMESTAMP"),
    bigquery.SchemaField("price", "FLOAT"),
    bigquery.SchemaField("freight_value", "FLOAT")
]

ORDER_PAYMENTS_SCHEMA = [
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("payment_sequential", "INTEGER"),
    bigquery.SchemaField("payment_type", "STRING"),
    bigquery.SchemaField("payment_installments", "INTEGER"),
    bigquery.SchemaField("payment_value", "FLOAT")
]

ORDER_REVIEWS_SCHEMA = [
    bigquery.SchemaField("review_id", "STRING"),
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("review_score", "INTEGER"),
    bigquery.SchemaField("review_comment_title", "STRING"),
    bigquery.SchemaField("review_comment_message", "STRING"),
    bigquery.SchemaField("review_creation_date", "TIMESTAMP"),
    bigquery.SchemaField("review_answer_timestamp", "TIMESTAMP")
]

ORDERS_SCHEMA = [
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("customer_id", "STRING"),
    bigquery.SchemaField("order_status", "STRING"),
    bigquery.SchemaField("order_purchase_timestamp", "TIMESTAMP"),
    bigquery.SchemaField("order_approved_at", "TIMESTAMP"),
    bigquery.SchemaField("order_delivered_carrier_date", "TIMESTAMP"),
    bigquery.SchemaField("order_delivered_customer_date", "TIMESTAMP"),
    bigquery.SchemaField("order_estimated_delivery_date", "TIMESTAMP")
]

PRODUCTS_SCHEMA = [
    bigquery.SchemaField("product_id", "STRING"),
    bigquery.SchemaField("product_category_name", "STRING"),
    bigquery.SchemaField("product_name_length", "INTEGER"),
    bigquery.SchemaField("product_description_length", "INTEGER"),
    bigquery.SchemaField("product_photos_qty", "INTEGER"),
    bigquery.SchemaField("product_weight_g", "INTEGER"),
    bigquery.SchemaField("product_length_cm", "INTEGER"),
    bigquery.SchemaField("product_height_cm", "INTEGER"),
    bigquery.SchemaField("product_width_cm", "INTEGER")
]

SELLERS_SCHEMA = [
    bigquery.SchemaField("seller_id", "STRING"),
    bigquery.SchemaField("seller_zip_code_prefix", "STRING"),
    bigquery.SchemaField("seller_city", "STRING"),
    bigquery.SchemaField("seller_state", "STRING")
]

PRODUCT_CATEGORY_TRANSLATION_SCHEMA = [
    bigquery.SchemaField("product_category_name", "STRING"),
    bigquery.SchemaField("product_category_name_english", "STRING")
]

