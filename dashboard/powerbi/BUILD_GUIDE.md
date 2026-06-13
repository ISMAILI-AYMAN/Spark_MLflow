# Power BI — Optional Build Guide

Use this if you want a local `.pbix` file in addition to the committed screenshots.

## Prerequisites

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
- Pipeline already run (`python scripts/run_pipeline.py`)

## Option A — Import CSVs (recommended, no Postgres driver needed)

1. Open Power BI Desktop → **Get data** → **Text/CSV**
2. Import all files from `dashboard/powerbi/data/`:
   - `kpi_monthly_revenue.csv`
   - `kpi_cohort_retention.csv`
   - `kpi_churn_rate.csv`
   - `kpi_category_mix.csv`
   - `kpi_top_sellers.csv`
   - `kpi_delivery_performance.csv`
   - `kpi_regional_orders.csv`
   - `kpi_payment_mix.csv`
   - `kpi_review_score.csv`
   - `kpi_aov.csv`
3. Create relationships only where needed (most tables stand alone)

## Option B — Direct PostgreSQL connection

| Setting | Value |
|---------|-------|
| Server | `localhost:5433` |
| Database | `olist` |
| Schema | `gold` |

Import the same `gold.kpi_*` tables listed in Option A.

## Suggested pages (match screenshots)

### Page 1 — Executive Summary
- Line chart: `order_month` vs `total_revenue` (`kpi_monthly_revenue`)
- Cards: latest `total_revenue`, `order_count`, `revenue_growth_pct`, `avg_order_value`
- Column chart: `order_count` by month

### Page 2 — Cohorts & Retention
- Matrix: rows = `cohort_month`, columns = `period_number`, values = `retention_pct`
- Bar chart: top 15 `product_category` by `churn_rate_pct` (`kpi_churn_rate`)

### Page 3 — Sellers & Categories
- Pie: `category_revenue` by `product_category` (`kpi_category_mix`)
- Bar: `revenue_share_pct` by `revenue_decile` (`kpi_top_sellers`)
- Bar: top 10 states by `total_revenue` (`kpi_regional_orders`)

### Page 4 — Delivery & Reviews
- Bar: `avg_delivery_delay_days` by `customer_state` (`kpi_delivery_performance`)
- Bar: `avg_review_score` by `delivery_bucket` (`kpi_review_score`)
- Pie: `value_share_pct` by `payment_type` (`kpi_payment_mix`)

## Save locally

Save as `dashboard/powerbi/olist_executive.pbix` (gitignored — keep screenshots in repo for GitHub).

Export page PNGs to `screenshots/` to refresh README visuals.

## Sample DAX (Executive page)

```dax
Latest Revenue =
CALCULATE(
    MAX('kpi_monthly_revenue'[total_revenue]),
    'kpi_monthly_revenue'[order_month] = MAX('kpi_monthly_revenue'[order_month])
)
```
