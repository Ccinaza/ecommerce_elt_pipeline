{{ config(materialized='table') }}


with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

state_metrics as (
    select
        customers.customer_state,
        count(distinct orders.order_id) as total_orders,
        count(distinct customers.customer_id) as total_customers,
        sum(order_items.price) as total_revenue
    from {{ ref('stg_customers') }} customers
    join {{ ref('stg_orders') }} orders using (customer_id)
    join {{ ref('stg_order_items') }} order_items using (order_id)
    where orders.order_status = 'delivered' and orders.order_delivered_customer_date is not null
    group by 1
)

select * from state_metrics

