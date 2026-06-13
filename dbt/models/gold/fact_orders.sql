with order_items_agg as (
    select
        order_id,
        sum(price) as order_revenue,
        sum(freight_value) as order_freight,
        sum(total_item_value) as order_total_value,
        count(*) as item_count,
        count(distinct product_id) as distinct_products,
        count(distinct seller_id) as distinct_sellers,
        mode() within group (order by product_category_en) as primary_category
    from {{ ref('silver_order_items_enriched') }}
    group by order_id
)
select
    o.order_id,
    o.customer_id,
    o.customer_unique_id,
    o.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    date_trunc('month', o.order_purchase_timestamp)::date as order_month,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    o.delivery_delay_days,
    coalesce(oi.order_revenue, 0) as order_revenue,
    coalesce(oi.order_freight, 0) as order_freight,
    coalesce(oi.order_total_value, 0) as order_total_value,
    coalesce(oi.item_count, 0) as item_count,
    coalesce(oi.distinct_products, 0) as distinct_products,
    coalesce(oi.distinct_sellers, 0) as distinct_sellers,
    oi.primary_category,
    r.avg_review_score,
    p.has_credit_card,
    p.has_boleto,
    p.max_installments
from {{ ref('silver_orders_enriched') }} o
left join order_items_agg oi on o.order_id = oi.order_id
left join {{ ref('silver_reviews_agg') }} r on o.order_id = r.order_id
left join {{ ref('silver_payments_agg') }} p on o.order_id = p.order_id
