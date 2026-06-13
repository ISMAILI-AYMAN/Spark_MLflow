select
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_state,
    c.customer_city,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    case
        when o.order_delivered_customer_date is not null
             and o.order_estimated_delivery_date is not null
        then extract(day from o.order_delivered_customer_date - o.order_estimated_delivery_date)
    end as delivery_delay_days
from {{ ref('bronze_orders') }} o
left join {{ ref('bronze_customers') }} c on o.customer_id = c.customer_id
