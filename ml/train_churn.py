"""Train and evaluate customer churn models with MLflow tracking."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from dotenv import load_dotenv
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    auc,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sqlalchemy import create_engine, text
from xgboost import XGBClassifier

load_dotenv(override=True)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(__file__).parent / "config.yaml"


def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "olist")
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_secret")
    return create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{db}")


def ensure_feature_view(engine) -> None:
    sql_path = Path(__file__).parent / "features" / "churn_features.sql"
    sql = sql_path.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS ml"))
        conn.execute(text(f"CREATE OR REPLACE VIEW ml.churn_features AS {sql}"))


def load_features(engine) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM ml.churn_features", engine)


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    numeric = [
        "frequency",
        "monetary",
        "avg_order_value",
        "avg_review_score",
        "avg_delivery_delay_days",
        "max_installments",
        "customer_tenure_days",
        "uses_credit_card",
        "uses_boleto",
    ]
    categorical = ["customer_state", "top_category"]
    return ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]),
                numeric,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical,
            ),
        ]
    )


def evaluate_model(name: str, pipeline: Pipeline, X, y, cv_folds: int) -> dict[str, float]:
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    y_proba = cross_val_predict(pipeline, X, y, cv=cv, method="predict_proba")[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    metrics = {
        "auc": float(roc_auc_score(y, y_proba)),
        "precision": float(precision_score(y, y_pred, zero_division=0)),
        "recall": float(recall_score(y, y_pred, zero_division=0)),
        "f1": float(f1_score(y, y_pred, zero_division=0)),
        "accuracy": float(accuracy_score(y, y_pred)),
    }
    print(f"\n{name} CV metrics: {metrics}")
    return metrics


def log_confusion_and_roc(model_name: str, y_true, y_proba) -> None:
    y_pred = (y_proba >= 0.5).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"{model_name} Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    mlflow.log_figure(fig, f"{model_name}_confusion_matrix.png")
    plt.close(fig)

    fpr, tpr, _ = roc_curve(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, label=f"AUC = {auc(fpr, tpr):.3f}")
    ax.plot([0, 1], [0, 1], "k--")
    ax.set_title(f"{model_name} ROC Curve")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    ax.legend()
    mlflow.log_figure(fig, f"{model_name}_roc_curve.png")
    plt.close(fig)

    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    mlflow.log_dict(report, f"{model_name}_classification_report.json")


def main() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(config["mlflow_experiment"])

    engine = get_engine()
    ensure_feature_view(engine)
    df = load_features(engine)

    target = "is_churned"
    feature_cols = [c for c in df.columns if c not in ("customer_unique_id", target)]
    X = df[feature_cols]
    y = df[target].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config["test_size"], random_state=config["random_state"], stratify=y
    )

    preprocessor = build_preprocessor(df)
    cv_folds = config["cv_folds"]

    models: dict[str, Pipeline] = {
        "logistic_regression": Pipeline([
            ("prep", preprocessor),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]),
        "xgboost": Pipeline([
            ("prep", preprocessor),
            (
                "clf",
                XGBClassifier(
                    n_estimators=200,
                    max_depth=5,
                    learning_rate=0.1,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    eval_metric="logloss",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]),
    }

    best_name = ""
    best_auc = -1.0
    all_results: dict[str, dict] = {}

    for name, pipeline in models.items():
        if name not in config.get("models", list(models.keys())):
            continue

        cv_metrics = evaluate_model(name, pipeline, X, y, cv_folds)

        with mlflow.start_run(run_name=name):
            mlflow.log_params({"model": name, "cv_folds": cv_folds})
            for k, v in cv_metrics.items():
                mlflow.log_metric(f"cv_{k}", v)

            pipeline.fit(X_train, y_train)
            test_proba = pipeline.predict_proba(X_test)[:, 1]
            test_pred = (test_proba >= 0.5).astype(int)
            test_metrics = {
                "test_auc": float(roc_auc_score(y_test, test_proba)),
                "test_precision": float(precision_score(y_test, test_pred, zero_division=0)),
                "test_recall": float(recall_score(y_test, test_pred, zero_division=0)),
                "test_f1": float(f1_score(y_test, test_pred, zero_division=0)),
            }
            for k, v in test_metrics.items():
                mlflow.log_metric(k, v)

            log_confusion_and_roc(name, y_test, test_proba)
            try:
                mlflow.sklearn.log_model(pipeline, name="model")
            except Exception as exc:
                print(f"Warning: model registry log skipped: {exc}")

            all_results[name] = {**cv_metrics, **test_metrics}

            if cv_metrics["auc"] > best_auc:
                best_auc = cv_metrics["auc"]
                best_name = name

    results = {
        "best_model": best_name,
        "best_cv_auc": round(best_auc, 4),
        "models": all_results,
    }

    import json

    results_path = PROJECT_ROOT / "ml" / "results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nBest model: {best_name} (CV AUC={best_auc:.4f})")


if __name__ == "__main__":
    main()
