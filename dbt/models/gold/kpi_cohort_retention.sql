with customer_cohort as (
    select
        customer_unique_id,
        date_trunc('month', min(order_purchase_timestamp))::date as cohort_month
    from {{ ref('fact_orders') }}
    where order_status = 'delivered'
    group by customer_unique_id
),
order_periods as (
    select
        f.customer_unique_id,
        cc.cohort_month,
        date_trunc('month', f.order_purchase_timestamp)::date as order_month,
        count(distinct f.order_id) as orders
    from {{ ref('fact_orders') }} f
    inner join customer_cohort cc on f.customer_unique_id = cc.customer_unique_id
    where f.order_status = 'delivered'
    group by 1, 2, 3
),
cohort_size as (
    select cohort_month, count(distinct customer_unique_id) as cohort_customers
    from customer_cohort
    group by cohort_month
)
select
    op.cohort_month,
    cs.cohort_customers,
    (extract(year from age(op.order_month, op.cohort_month)) * 12
     + extract(month from age(op.order_month, op.cohort_month)))::int as period_number,
    count(distinct op.customer_unique_id) as active_customers,
    round(
        100.0 * count(distinct op.customer_unique_id) / nullif(cs.cohort_customers, 0),
        2
    ) as retention_pct
from order_periods op
inner join cohort_size cs on op.cohort_month = cs.cohort_month
group by op.cohort_month, cs.cohort_customers, period_number, op.order_month
order by op.cohort_month, period_number
