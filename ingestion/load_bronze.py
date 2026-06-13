"""Load Olist raw CSVs into PostgreSQL bronze schema (idempotent)."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "olist"

TABLE_FILES: dict[str, str] = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "olist")
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_secret")
    url = f"postgresql+pg8000://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def load_table(engine, table_name: str, csv_file: str) -> int:
    path = RAW_DIR / csv_file
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV: {path}. See data/raw/olist/README.md")

    df = pd.read_csv(path, low_memory=False)
    full_name = f"bronze.{table_name}"

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {full_name} CASCADE"))
        df.to_sql(
            table_name,
            conn,
            schema="bronze",
            index=False,
            if_exists="replace",
            method="multi",
            chunksize=5000,
        )

    return len(df)


def main() -> None:
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))

    total = 0
    for table, csv_file in TABLE_FILES.items():
        rows = load_table(engine, table, csv_file)
        print(f"Loaded bronze.{table}: {rows:,} rows")
        total += rows

    print(f"Done. {total:,} total rows loaded across {len(TABLE_FILES)} tables.")


if __name__ == "__main__":
    main()
