select
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value as total_item_value,
    p.product_category_name,
    coalesce(ct.product_category_name_english, p.product_category_name) as product_category_en,
    s.seller_state,
    s.seller_city
from {{ ref('bronze_order_items') }} oi
left join {{ ref('bronze_products') }} p on oi.product_id = p.product_id
left join {{ ref('bronze_category_translation') }} ct
    on p.product_category_name = ct.product_category_name
left join {{ ref('bronze_sellers') }} s on oi.seller_id = s.seller_id
