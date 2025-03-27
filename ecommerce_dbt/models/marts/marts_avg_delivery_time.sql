with delivery_stats AS (
  select
    order_id,
    delivery_time_days,
    avg_delivery_time_days,
    COUNT(*) OVER() AS total_orders,
    SUM(CASE WHEN delivery_time_days > avg_delivery_time_days THEN 1 ELSE 0 END) OVER() AS orders_above_avg,
    SUM(CASE WHEN delivery_time_days <= avg_delivery_time_days THEN 1 ELSE 0 END) OVER() AS orders_below_avg
  from {{ ref('int_avg_delivery_time') }}
)
select
  AVG(avg_delivery_time_days) AS avg_delivery_time,
  MAX(orders_above_avg) AS orders_above_avg,
  MAX(orders_below_avg) AS orders_below_avg,
  MAX(orders_above_avg) / MAX(total_orders) * 100 AS percent_above_avg,
  MAX(orders_below_avg) / MAX(total_orders) * 100 AS percent_below_avg
from delivery_stats