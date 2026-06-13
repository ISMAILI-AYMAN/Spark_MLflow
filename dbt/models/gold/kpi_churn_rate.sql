with customer_activity as (
    select
        customer_unique_id,
        customer_state,
        primary_category,
        max(order_purchase_timestamp) as last_order_at,
        count(distinct order_id) as total_orders,
        sum(order_total_value) as total_spend
    from {{ ref('fact_orders') }}
    where order_status = 'delivered'
    group by customer_unique_id, customer_state, primary_category
),
reference_date as (
    select max(order_purchase_timestamp)::date as max_date
    from {{ ref('fact_orders') }}
)
select
    ca.customer_state,
    ca.primary_category as product_category,
    count(*) as customer_count,
    sum(case when ca.last_order_at < rd.max_date - interval '90 days' then 1 else 0 end) as churned_customers,
    round(
        100.0 * sum(case when ca.last_order_at < rd.max_date - interval '90 days' then 1 else 0 end)
        / nullif(count(*), 0),
        2
    ) as churn_rate_pct
from customer_activity ca
cross join reference_date rd
group by ca.customer_state, ca.primary_category
order by churn_rate_pct desc
