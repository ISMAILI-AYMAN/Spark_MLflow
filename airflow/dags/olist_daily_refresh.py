"""Airflow DAG: daily Olist pipeline refresh (load -> dbt -> churn training)."""

from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

PROJECT_ROOT = os.environ.get("OLIST_PROJECT_ROOT", "/opt/olist")


def load_bronze_task() -> None:
    import sys

    sys.path.insert(0, PROJECT_ROOT)
    from ingestion.load_bronze import main

    main()


def train_churn_task() -> None:
    import sys

    sys.path.insert(0, PROJECT_ROOT)
    from ml.train_churn import main

    main()


default_args = {
    "owner": "olist",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dbt_env = (
    f"export POSTGRES_HOST={os.environ.get('POSTGRES_HOST', 'olist-postgres')} "
    f"POSTGRES_PORT={os.environ.get('POSTGRES_PORT', '5432')} "
    f"POSTGRES_DB={os.environ.get('POSTGRES_DB', 'olist')} "
    f"POSTGRES_USER={os.environ.get('POSTGRES_USER', 'olist')} "
    f"POSTGRES_PASSWORD={os.environ.get('POSTGRES_PASSWORD', 'olist_secret')}"
)

with DAG(
    dag_id="olist_daily_refresh",
    default_args=default_args,
    description="Load bronze, run dbt, train churn model",
    schedule_interval="@daily",
    start_date=datetime(2018, 1, 1),
    catchup=False,
    tags=["olist", "dbt", "ml"],
) as dag:
    load_bronze = PythonOperator(
        task_id="load_bronze",
        python_callable=load_bronze_task,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{dbt_env} && cd {PROJECT_ROOT}/dbt && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{dbt_env} && cd {PROJECT_ROOT}/dbt && dbt test --profiles-dir .",
    )

    train_churn = PythonOperator(
        task_id="train_churn_model",
        python_callable=train_churn_task,
    )

    load_bronze >> dbt_run >> dbt_test >> train_churn
