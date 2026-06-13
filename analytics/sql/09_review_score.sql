select delivery_bucket, order_count, avg_review_score, avg_delivery_delay_days
from gold.kpi_review_score
order by avg_review_score desc;
