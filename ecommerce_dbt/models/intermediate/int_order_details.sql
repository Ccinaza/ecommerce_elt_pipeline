{{ config(materialized='table') }}

with orders as (
    select * from {{ ref("stg_orders") }}
),

order_items as (
    select * from {{ ref("stg_order_items") }}
),

order_details as (
    select
        orders.order_id,
        orders.customer_id,
        orders.order_status,
        orders.order_purchase_timestamp,
        count(distinct order_items.order_item_id) as number_of_items,
        sum(order_items.price) as total_order_value,
        sum(order_items.freight_value) as total_freight_value
    from orders
    left join order_items on orders.order_id = order_items.order_id
    group by 1, 2, 3, 4
)

select * from order_details