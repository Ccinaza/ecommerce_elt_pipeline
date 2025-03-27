{{ config(materialized='table') }}

with product_performance as (
    select * from {{ ref('int_product_performance') }}
)

select
    product_category_name_english,
    sum(total_revenue) as total_sales,
    count(distinct product_id) as unique_products,
    avg(average_price) as avg_product_price
from product_performance
group by 1
order by total_sales desc
