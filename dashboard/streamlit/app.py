"""Streamlit executive dashboard for Olist analytics."""

from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(override=True)

st.set_page_config(page_title="Olist Analytics", layout="wide", page_icon="📊")


@st.cache_resource
def get_engine():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "olist")
    user = os.getenv("POSTGRES_USER", "olist")
    password = os.getenv("POSTGRES_PASSWORD", "olist_secret")
    return create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{db}")


@st.cache_data(ttl=300)
def load_query(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, get_engine())


def kpi_cards(df: pd.DataFrame) -> None:
    latest = df.iloc[-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Latest Month Revenue", f"R$ {latest['total_revenue']:,.0f}")
    c2.metric("Orders", f"{int(latest['order_count']):,}")
    c3.metric("MoM Revenue Growth", f"{latest['revenue_growth_pct']:.1f}%")
    c4.metric("AOV", f"R$ {latest['avg_order_value']:.2f}")


def main() -> None:
    st.title("Olist Revenue & Retention Analytics")
    st.caption("Executive dashboard over 100K+ Brazilian e-commerce orders")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Executive Summary",
        "Cohorts & Retention",
        "Sellers & Categories",
        "Delivery & Reviews",
    ])

    with tab1:
        rev = load_query("SELECT * FROM gold.kpi_monthly_revenue ORDER BY order_month")
        kpi_cards(rev)
        fig = px.line(rev, x="order_month", y="total_revenue", markers=True, title="Monthly Revenue")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(rev, x="order_month", y="order_count", title="Monthly Order Volume")
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        cohort = load_query(
            "SELECT * FROM gold.kpi_cohort_retention WHERE period_number <= 6 ORDER BY cohort_month, period_number"
        )
        heat = cohort.pivot(index="cohort_month", columns="period_number", values="retention_pct")
        fig = px.imshow(heat, labels=dict(x="Period", y="Cohort", color="Retention %"), aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

        churn = load_query(
            "SELECT * FROM gold.kpi_churn_rate ORDER BY churn_rate_pct DESC LIMIT 15"
        )
        fig2 = px.bar(
            churn,
            x="product_category",
            y="churn_rate_pct",
            color="customer_state",
            title="90-Day Churn Rate by Category & State",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            cats = load_query("SELECT * FROM gold.kpi_category_mix ORDER BY category_revenue DESC LIMIT 12")
            fig = px.pie(cats, names="product_category", values="category_revenue", title="Revenue by Category")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            sellers = load_query("SELECT * FROM gold.kpi_top_sellers ORDER BY revenue_decile")
            fig = px.bar(sellers, x="revenue_decile", y="revenue_share_pct", title="Seller Revenue Concentration (Deciles)")
            st.plotly_chart(fig, use_container_width=True)

        regional = load_query("SELECT * FROM gold.kpi_regional_orders ORDER BY total_revenue DESC")
        fig3 = px.bar(regional.head(10), x="customer_state", y="total_revenue", title="Top 10 States by Revenue")
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        delivery = load_query("SELECT * FROM gold.kpi_delivery_performance ORDER BY avg_delivery_delay_days DESC")
        fig = px.bar(delivery.head(10), x="customer_state", y="avg_delivery_delay_days", title="Avg Delivery Delay by State")
        st.plotly_chart(fig, use_container_width=True)

        reviews = load_query("SELECT * FROM gold.kpi_review_score ORDER BY avg_review_score DESC")
        fig2 = px.bar(reviews, x="delivery_bucket", y="avg_review_score", title="Review Score vs Delivery Performance")
        st.plotly_chart(fig2, use_container_width=True)

        payments = load_query("SELECT * FROM gold.kpi_payment_mix")
        fig3 = px.pie(payments, names="payment_type", values="value_share_pct", title="Payment Mix")
        st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    main()
