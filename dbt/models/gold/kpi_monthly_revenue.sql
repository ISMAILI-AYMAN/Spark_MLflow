with monthly as (
    select
        order_month,
        count(distinct order_id) as order_count,
        count(distinct customer_unique_id) as customer_count,
        sum(order_total_value) as total_revenue,
        avg(order_total_value) as avg_order_value
    from {{ ref('fact_orders') }}
    where order_status = 'delivered'
      and order_month is not null
    group by order_month
)
select
    order_month,
    order_count,
    customer_count,
    round(total_revenue::numeric, 2) as total_revenue,
    round(avg_order_value::numeric, 2) as avg_order_value,
    round(
        100.0 * (total_revenue - lag(total_revenue) over (order by order_month))
        / nullif(lag(total_revenue) over (order by order_month), 0),
        2
    ) as revenue_growth_pct,
    round(
        100.0 * (order_count - lag(order_count) over (order by order_month))
        / nullif(lag(order_count) over (order by order_month), 0),
        2
    ) as order_growth_pct
from monthly
order by order_month
