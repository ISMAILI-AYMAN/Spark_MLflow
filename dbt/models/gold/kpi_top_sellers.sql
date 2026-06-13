with seller_revenue as (
    select
        seller_id,
        sum(total_item_value) as seller_revenue,
        count(distinct order_id) as order_count
    from {{ ref('fact_order_items') }}
    group by seller_id
),
ranked as (
    select
        *,
        ntile(10) over (order by seller_revenue desc) as revenue_decile,
        sum(seller_revenue) over () as total_marketplace_revenue
    from seller_revenue
)
select
    revenue_decile,
    count(*) as seller_count,
    round(sum(seller_revenue)::numeric, 2) as segment_revenue,
    round(100.0 * sum(seller_revenue) / max(total_marketplace_revenue), 2) as revenue_share_pct,
    round(avg(seller_revenue)::numeric, 2) as avg_seller_revenue
from ranked
group by revenue_decile
order by revenue_decile
