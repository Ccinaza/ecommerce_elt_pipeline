{{ config(materialized='table') }}

with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

product_category_names as (
    select * from {{ ref('stg_product_category_translation') }}
),

-- Calculate product performance metrics
product_metrics as (
    select
        products.product_id,
        product_category_names.product_category_name_english,
        count(distinct order_items.order_id) as number_of_orders,
        sum(order_items.price) as total_revenue,
        avg(order_items.price) as average_price,
        sum(order_items.freight_value) as total_freight_cost
    from products
    left join order_items on products.product_id = order_items.product_id
    left join product_category_names 
        on products.product_category_name = product_category_names.product_category_name
    group by 1,2
)

select * from product_metrics
