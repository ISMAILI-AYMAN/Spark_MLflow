# Business Insights — Olist E-commerce Analytics

Data snapshot: **99,441 orders** | **96,278 delivered** | Reference period ends **2018-08-29**

## Key findings

### 1. Revenue plateaued in late 2018
- August 2018 revenue: **R$ 985,492** (−4.1% MoM)
- June 2018 saw the largest recent drop: **−10.4% MoM**
- **Action:** Investigate seasonality and marketing spend in Q2–Q3 2018; set rolling 3-month revenue targets.

### 2. Top category concentration — health & beauty
- **health_beauty** leads with **9.2%** of marketplace revenue
- **89%** 90-day churn rate in this category (vs ~91% marketplace average)
- **Action:** Launch a health_beauty re-engagement campaign (email + voucher) for customers inactive 60+ days.

### 3. Cohort retention collapses after month 0
- Period-0 (acquisition month) retention: **100%**
- Period-1 retention: **5.5%** average across cohorts
- **Action:** Introduce a 30-day post-purchase nurture flow; A/B test second-purchase discount.

### 4. Seller revenue is highly concentrated
- Top **10%** of sellers (decile 1) capture **66.8%** of total seller revenue
- Long-tail sellers contribute minimal GMV
- **Action:** Tiered seller success program — prioritize onboarding and logistics support for mid-tier sellers.

### 5. Payment mix favors credit cards
- **Credit card:** 78.3% of payment value
- **Boleto:** 17.9%
- **Action:** Optimize installment options for high-AOV categories; monitor boleto conversion in northern states.

### 6. Delivery delays correlate with lower reviews
- Orders **8+ days late** average materially lower review scores than on-time deliveries
- **Action:** Flag sellers/states with highest avg delivery delay for logistics review.

### 7. Churn model performance (ML)
- **XGBoost** classifier: **0.76 AUC** (5-fold CV), **99.5% recall** at default threshold
- Top features: order frequency, monetary value, category, payment behavior
- **Action:** Use model scores to prioritize retention outreach for high-value customers with low frequency.

## Recommended next steps

1. Deploy Streamlit / Power BI dashboards for weekly KPI reviews
2. Test retention campaigns on health_beauty cohort (highest revenue + high churn)
3. Expand pipeline with LTV model and 7-day demand forecast (full version)
