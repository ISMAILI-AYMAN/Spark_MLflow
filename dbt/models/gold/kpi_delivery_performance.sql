select
    customer_state,
    count(distinct order_id) as order_count,
    round(avg(delivery_delay_days)::numeric, 2) as avg_delivery_delay_days,
    round(percentile_cont(0.5) within group (order by delivery_delay_days)::numeric, 2) as median_delivery_delay_days,
    sum(case when delivery_delay_days > 0 then 1 else 0 end) as late_deliveries,
    round(
        100.0 * sum(case when delivery_delay_days > 0 then 1 else 0 end) / nullif(count(*), 0),
        2
    ) as late_delivery_pct
from {{ ref('fact_orders') }}
where order_status = 'delivered'
  and delivery_delay_days is not null
group by customer_state
order by avg_delivery_delay_days desc
