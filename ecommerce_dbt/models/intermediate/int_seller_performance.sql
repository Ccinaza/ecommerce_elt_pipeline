{{ config(materialized='table') }}

with sellers as (
    select * from {{ ref('stg_sellers') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

-- Calculate seller performance metrics
seller_metrics as (
    select
        sellers.seller_id,
        sellers.seller_state,
        count(distinct order_items.order_id) as orders_fulfilled,
        sum(order_items.price) as total_revenue,
        avg(order_items.price) as average_order_value,
        count(distinct order_items.product_id) as unique_products_sold
    from sellers
    left join order_items on sellers.seller_id = order_items.seller_id
    group by 1,2
)

select * from seller_metrics
