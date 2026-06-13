-- Cohort retention by acquisition month
-- Source: gold.kpi_cohort_retention (dbt model)

select
    cohort_month,
    period_number,
    cohort_customers,
    active_customers,
    retention_pct
from gold.kpi_cohort_retention
where period_number <= 12
order by cohort_month, period_number;
