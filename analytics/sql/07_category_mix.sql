select product_category, category_revenue, revenue_share_pct
from gold.kpi_category_mix
order by category_revenue desc
limit 15;
