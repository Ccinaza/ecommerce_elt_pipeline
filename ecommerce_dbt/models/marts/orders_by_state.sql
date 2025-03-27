{{ config(materialized='table') }}

with state_metrics as (
    select * from {{ ref('int_state_metrics') }}
)

select
    customer_state,
    total_orders,
    RANK() OVER (ORDER BY total_orders DESC) AS order_rank,
    total_customers,
    total_revenue,
    total_orders / total_customers as orders_per_customer
from state_metrics
order by total_orders desc
