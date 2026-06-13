with dates as (
    select distinct date_trunc('day', order_purchase_timestamp)::date as date_day
    from {{ ref('silver_orders_enriched') }}
    where order_purchase_timestamp is not null
)
select
    date_day,
    extract(year from date_day)::int as year,
    extract(month from date_day)::int as month,
    extract(quarter from date_day)::int as quarter,
    to_char(date_day, 'YYYY-MM') as year_month
from dates
