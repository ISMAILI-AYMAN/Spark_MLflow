select
    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state,
    min(o.order_purchase_timestamp) as first_order_at,
    max(o.order_purchase_timestamp) as last_order_at,
    count(distinct o.order_id) as total_orders
from {{ ref('bronze_customers') }} c
left join {{ ref('silver_orders_enriched') }} o on c.customer_id = o.customer_id
group by 1, 2, 3, 4, 5
