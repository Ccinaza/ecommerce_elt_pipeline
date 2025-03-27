{{ config(materialized='table') }}

with order_delivery_times as(
    select
        order_id,
        timestamp_diff(order_delivered_customer_date, order_purchase_timestamp, DAY) AS delivery_time_days
    from
        {{ ref('stg_orders') }}
    where
        order_status = 'delivered' and order_delivered_customer_date is not null
)
select
    order_id, 
    delivery_time_days,
    avg(delivery_time_days) over() as avg_delivery_time_days 
from order_delivery_times


