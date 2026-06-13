with payment_totals as (
    select
        payment_type,
        sum(payment_value) as total_value,
        count(*) as payment_count
    from {{ ref('bronze_order_payments') }}
    group by payment_type
)
select
    payment_type,
    payment_count,
    round(total_value::numeric, 2) as total_value,
    round(100.0 * total_value / sum(total_value) over (), 2) as value_share_pct,
    round(100.0 * payment_count / sum(payment_count) over (), 2) as count_share_pct
from payment_totals
order by total_value desc
