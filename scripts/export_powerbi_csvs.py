"""Export gold KPI tables to CSV for Power BI Desktop import."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)

OUT_DIR = Path(__file__).resolve().parents[1] / "dashboard" / "powerbi" / "data"

TABLES = [
    "kpi_monthly_revenue",
    "kpi_cohort_retention",
    "kpi_churn_rate",
    "kpi_aov",
    "kpi_delivery_performance",
    "kpi_top_sellers",
    "kpi_category_mix",
    "kpi_payment_mix",
    "kpi_review_score",
    "kpi_regional_orders",
]


def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "olist")
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_secret")
    return create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{db}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = get_engine()

    for table in TABLES:
        df = pd.read_sql(text(f"SELECT * FROM gold.{table}"), engine)
        path = OUT_DIR / f"{table}.csv"
        df.to_csv(path, index=False)
        print(f"Exported {len(df):,} rows -> {path}")

    print(f"\nDone. Import these CSVs in Power BI Desktop (see dashboard/powerbi/BUILD_GUIDE.md).")


if __name__ == "__main__":
    main()
