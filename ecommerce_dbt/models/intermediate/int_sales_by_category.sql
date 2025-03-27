{{ config(materialized='table') }}

with sales as (
select 
    o.order_id,
    o.order_status,
    o.order_delivered_customer_date,
    oi.product_id,
    oi.price,
    pt.product_category_name_english as product_category
from {{ ref('stg_orders') }} o
join {{ ref('stg_order_items') }} oi on o.order_id = oi.order_id
join {{ ref('stg_products') }} p on oi.product_id = p.product_id
join {{ ref('stg_product_category_translation') }} pt on p.product_category_name = pt.product_category_name
)
select 
    product_category,
    sum(price) as total_sales
from sales
where order_status = 'delivered' and order_delivered_customer_date is not null
group by product_category
order by total_sales