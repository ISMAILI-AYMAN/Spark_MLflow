-- Monthly revenue and order growth (MoM)
-- Source: gold.kpi_monthly_revenue (dbt model)

select
    order_month,
    order_count,
    total_revenue,
    revenue_growth_pct,
    order_growth_pct
from gold.kpi_monthly_revenue
order by order_month;
