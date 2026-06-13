# Power BI Executive Dashboard

## DA portfolio deliverable

The **official DA proof** for this repo is:

1. **Screenshots** in [screenshots/](screenshots/) (committed to GitHub)
2. **CSV exports** in [data/](data/) (regenerate with `python scripts/export_powerbi_csvs.py`)
3. **Streamlit live demo** at [../streamlit/app.py](../streamlit/app.py)

See [DA_DELIVERABLE.md](DA_DELIVERABLE.md) for resume wording.

A local `.pbix` is **optional** — build instructions: [BUILD_GUIDE.md](BUILD_GUIDE.md)

## Connection (if building .pbix from Postgres)

| Setting | Value |
|---------|-------|
| Server | `localhost:5433` |
| Database | `olist` |
| Schema | `gold` |

## Pages (match screenshots)

1. **Executive Summary** — `kpi_monthly_revenue`
2. **Cohorts & Retention** — `kpi_cohort_retention`, `kpi_churn_rate`
3. **Sellers & Categories** — `kpi_category_mix`, `kpi_top_sellers`, `kpi_regional_orders`
4. **Delivery & Reviews** — `kpi_delivery_performance`, `kpi_review_score`, `kpi_payment_mix`

## Refresh workflow

```bash
python scripts/run_pipeline.py
python scripts/export_powerbi_csvs.py
python scripts/generate_dashboard_screenshots.py
```
