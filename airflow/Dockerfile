FROM apache/airflow:2.8.1-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    "dbt-core>=1.8,<2" \
    "dbt-postgres>=1.8,<2" \
    pandas \
    pg8000 \
    python-dotenv \
    sqlalchemy \
    scikit-learn \
    xgboost \
    mlflow \
    pyyaml \
    matplotlib \
    seaborn

ENV OLIST_PROJECT_ROOT=/opt/olist
