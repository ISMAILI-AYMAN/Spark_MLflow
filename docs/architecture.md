# Olist Analytics Platform — Architecture

## Overview

End-to-end medallion analytics platform for the Olist Brazilian e-commerce dataset (~100K orders).

## Data flow

```mermaid
flowchart TB
    CSV[Raw Olist CSVs] --> Loader[ingestion/load_bronze.py]
    Loader --> Bronze[bronze schema]
    Bronze --> dbt[dbt models]
    dbt --> Silver[silver schema]
    Silver --> Gold[gold schema]
    Gold --> KPIs[gold.kpi_* tables]
    KPIs --> PBI[Power BI]
    KPIs --> ST[Streamlit]
    KPIs --> ML[Churn ML]
    AF[Airflow DAG] --> Loader
    AF --> dbt
    AF --> ML
    ML --> MLflow[MLflow]
```

## Schemas

| Schema | Purpose | Examples |
|--------|---------|----------|
| `bronze` | Raw CSV loads | `customers`, `orders`, `order_items` |
| `silver` | Cleaned joins | `orders_enriched`, `order_items_enriched` |
| `gold` | Analytics marts | `fact_orders`, `kpi_monthly_revenue` |
| `ml` | Feature views | `churn_features` |

## Orchestration

- **Local:** `python scripts/run_pipeline.py`
- **Airflow:** `airflow/dags/olist_daily_refresh.py` (daily schedule)

## Infrastructure

Docker Compose services:
- **postgres** — warehouse (port 5432)
- **mlflow** — experiment tracking (port 5000)
- **streamlit** — dashboard demo (port 8501)
