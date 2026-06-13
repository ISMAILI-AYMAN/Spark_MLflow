select
    customer_state,
    count(distinct order_id) as order_count,
    count(distinct customer_unique_id) as customer_count,
    round(sum(order_total_value)::numeric, 2) as total_revenue,
    round(avg(order_total_value)::numeric, 2) as avg_order_value
from {{ ref('fact_orders') }}
where order_status = 'delivered'
  and customer_state is not null
group by customer_state
order by total_revenue desc
