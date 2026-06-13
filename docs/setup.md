# Setup Guide

## Prerequisites

- Docker Desktop
- Python 3.11+ (dbt runs via Docker on Python 3.14+)
- [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) CSVs in `data/raw/olist/`

## Quick start

```bash
cp .env.example .env
docker compose up -d postgres mlflow
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
docker build -t olist-dbt -f dbt/Dockerfile .

python ingestion/load_bronze.py
python scripts/run_dbt.py run
python scripts/run_dbt.py test
python ml/train_churn.py

streamlit run dashboard/streamlit/app.py
# Or: docker compose up -d streamlit  -> http://localhost:8502
```

## Ports

| Service | Port |
|---------|------|
| PostgreSQL | **5433** (host) → 5432 (container) |
| MLflow (Docker) | 5001 |
| Streamlit | **8502** |

## Power BI

See [dashboard/powerbi/README.md](../dashboard/powerbi/README.md).

## Airflow

Mount this repo and set `OLIST_PROJECT_ROOT`. DAG: `olist_daily_refresh`.

## Troubleshooting

**PostgreSQL `invalid length of startup packet` in logs:** Harmless — usually a non-Postgres client (browser, port scanner) hitting the port. Ignore unless connections fail.

**dbt fails locally:** Use `python scripts/run_dbt.py run` (Docker-based runner).

**Auth failed on port 5432:** Another Postgres instance may be running locally. This project uses **port 5433**.
