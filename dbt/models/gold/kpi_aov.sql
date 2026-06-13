select
    order_month,
    count(distinct order_id) as order_count,
    round(avg(order_total_value)::numeric, 2) as avg_order_value,
    round(sum(order_total_value)::numeric, 2) as total_revenue,
    round(avg(item_count)::numeric, 2) as avg_items_per_order
from {{ ref('fact_orders') }}
where order_status = 'delivered'
  and order_month is not null
group by order_month
order by order_month
