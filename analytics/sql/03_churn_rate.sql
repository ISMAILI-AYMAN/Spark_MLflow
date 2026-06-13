-- 90-day churn rate by category and region
-- Source: gold.kpi_churn_rate (dbt model)

select
    customer_state,
    product_category,
    customer_count,
    churned_customers,
    churn_rate_pct
from gold.kpi_churn_rate
order by churn_rate_pct desc
limit 20;
