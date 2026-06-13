select
    product_category_en as product_category,
    count(distinct order_id) as order_count,
    sum(total_item_value) as category_revenue,
    round(100.0 * sum(total_item_value) / sum(sum(total_item_value)) over (), 2) as revenue_share_pct
from {{ ref('fact_order_items') }}
where product_category_en is not null
group by product_category_en
order by category_revenue desc
