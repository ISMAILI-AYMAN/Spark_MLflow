"""Generate static dashboard preview images for README (Power BI placeholder screenshots)."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(override=True)

OUT_DIR = Path(__file__).resolve().parents[1] / "dashboard" / "powerbi" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "olist")
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_secret")
    return create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{db}")


def save(fig, name: str) -> None:
    path = OUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def main() -> None:
    engine = get_engine()
    sns.set_theme(style="whitegrid")

    rev = pd.read_sql("SELECT * FROM gold.kpi_monthly_revenue ORDER BY order_month", engine)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(rev["order_month"], rev["total_revenue"], marker="o")
    ax.set_title("Executive Summary: Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (R$)")
    fig.autofmt_xdate()
    save(fig, "01_executive_summary.png")

    cohort = pd.read_sql(
        "SELECT * FROM gold.kpi_cohort_retention WHERE period_number <= 6", engine
    )
    heat = cohort.pivot(index="cohort_month", columns="period_number", values="retention_pct")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heat.iloc[-12:], annot=True, fmt=".0f", cmap="YlGn", ax=ax)
    ax.set_title("Cohorts & Retention")
    save(fig, "02_cohort_retention.png")

    cats = pd.read_sql(
        "SELECT * FROM gold.kpi_category_mix ORDER BY category_revenue DESC LIMIT 10", engine
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=cats, x="category_revenue", y="product_category", ax=ax)
    ax.set_title("Sellers & Categories: Top Categories by Revenue")
    save(fig, "03_category_mix.png")

    delivery = pd.read_sql(
        "SELECT * FROM gold.kpi_delivery_performance ORDER BY avg_delivery_delay_days DESC LIMIT 10",
        engine,
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=delivery, x="customer_state", y="avg_delivery_delay_days", ax=ax)
    ax.set_title("Delivery & Reviews: Avg Delay by State")
    save(fig, "04_delivery_reviews.png")


if __name__ == "__main__":
    main()
