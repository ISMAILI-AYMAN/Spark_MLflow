select
    case
        when delivery_delay_days <= 0 then 'on_time_or_early'
        when delivery_delay_days between 1 and 3 then '1_3_days_late'
        when delivery_delay_days between 4 and 7 then '4_7_days_late'
        else '8_plus_days_late'
    end as delivery_bucket,
    count(distinct order_id) as order_count,
    round(avg(avg_review_score)::numeric, 2) as avg_review_score,
    round(avg(delivery_delay_days)::numeric, 2) as avg_delivery_delay_days
from {{ ref('fact_orders') }}
where order_status = 'delivered'
  and avg_review_score is not null
  and delivery_delay_days is not null
group by delivery_bucket
order by avg_review_score desc
