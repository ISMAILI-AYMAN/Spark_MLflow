-- Customer-level features for churn prediction (90-day inactivity label)
-- Materialized as view after dbt run; used by ml/train_churn.py

with customer_orders as (
    select
        customer_unique_id,
        customer_state,
        order_id,
        order_purchase_timestamp,
        order_total_value,
        avg_review_score,
        delivery_delay_days,
        primary_category,
        has_credit_card,
        has_boleto,
        max_installments
    from gold.fact_orders
    where order_status = 'delivered'
),
customer_agg as (
    select
        customer_unique_id,
        max(customer_state) as customer_state,
        min(order_purchase_timestamp) as first_order_at,
        max(order_purchase_timestamp) as last_order_at,
        count(distinct order_id) as order_count,
        sum(order_total_value) as total_spend,
        avg(order_total_value) as avg_order_value,
        avg(avg_review_score) as avg_review_score,
        avg(delivery_delay_days) as avg_delivery_delay_days,
        mode() within group (order by primary_category) as top_category,
        max(has_credit_card) as uses_credit_card,
        max(has_boleto) as uses_boleto,
        max(max_installments) as max_installments
    from customer_orders
    group by customer_unique_id
),
reference as (
    select max(order_purchase_timestamp)::date as ref_date
    from gold.fact_orders
)
select
    ca.customer_unique_id,
    ca.customer_state,
    ca.order_count as frequency,
    (r.ref_date - ca.last_order_at::date)::int as recency_days,
    ca.total_spend as monetary,
    ca.avg_order_value,
    ca.avg_review_score,
    ca.avg_delivery_delay_days,
    ca.top_category,
    ca.uses_credit_card,
    ca.uses_boleto,
    ca.max_installments,
    (ca.last_order_at::date - ca.first_order_at::date)::int as customer_tenure_days,
    case
        when ca.last_order_at < r.ref_date - interval '90 days' then 1
        else 0
    end as is_churned
from customer_agg ca
cross join reference r
where ca.order_count >= 1;
