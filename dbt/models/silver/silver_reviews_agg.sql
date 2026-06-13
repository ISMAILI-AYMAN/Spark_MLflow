select
    order_id,
    avg(review_score)::numeric(4, 2) as avg_review_score,
    min(review_score) as min_review_score,
    max(review_score) as max_review_score,
    count(*) as review_count
from {{ ref('bronze_order_reviews') }}
group by order_id
