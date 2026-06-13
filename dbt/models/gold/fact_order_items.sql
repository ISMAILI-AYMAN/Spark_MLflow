select
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    o.customer_unique_id,
    o.customer_state,
    o.order_purchase_timestamp,
    date_trunc('month', o.order_purchase_timestamp)::date as order_month,
    oi.product_category_en,
    oi.price,
    oi.freight_value,
    oi.total_item_value,
    oi.seller_state
from {{ ref('silver_order_items_enriched') }} oi
inner join {{ ref('silver_orders_enriched') }} o on oi.order_id = o.order_id
