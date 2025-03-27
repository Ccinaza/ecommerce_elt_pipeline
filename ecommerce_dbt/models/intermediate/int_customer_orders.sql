{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),

order_details as (
    select * from {{ ref('int_order_details') }}
),

-- Calculate customer metrics from their orders
customer_orders as (
    select
        customers.customer_id,
        customers.customer_unique_id,
        customers.customer_state,
        count(distinct order_details.order_id) as number_of_orders,
        sum(order_details.total_order_value) as total_customer_spend,
        min(order_details.order_purchase_timestamp) as first_order_date,
        max(order_details.order_purchase_timestamp) as last_order_date
    from customers
    left join order_details using (customer_id)
    group by 1,2,3
)

select * from customer_orders
