# Power BI Executive Dashboard

Connect Power BI Desktop to PostgreSQL `gold` schema after running the pipeline.

## Connection

- **Server:** `localhost:5432`
- **Database:** `olist`
- **Schema:** `gold`

## Recommended pages

1. **Executive Summary** — `kpi_monthly_revenue`, KPI cards for revenue/orders/AOV
2. **Cohorts & Retention** — `kpi_cohort_retention` matrix, `kpi_churn_rate`
3. **Sellers & Categories** — `kpi_category_mix`, `kpi_top_sellers`, `kpi_regional_orders`
4. **Delivery & Reviews** — `kpi_delivery_performance`, `kpi_review_score`, `kpi_payment_mix`

## Screenshots

Export page screenshots to `dashboard/powerbi/screenshots/` for the README.

Tables to import:
- `gold.kpi_monthly_revenue`
- `gold.kpi_cohort_retention`
- `gold.kpi_churn_rate`
- `gold.kpi_category_mix`
- `gold.kpi_top_sellers`
- `gold.kpi_delivery_performance`
- `gold.kpi_regional_orders`
