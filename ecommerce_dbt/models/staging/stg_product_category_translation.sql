{{ config(materialized='view') }}

select
    product_category_name,
    product_category_name_english
from {{ source('ecommerce', 'product_category_name_translation') }}
