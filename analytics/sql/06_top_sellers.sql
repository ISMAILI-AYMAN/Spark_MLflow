select revenue_decile, seller_count, segment_revenue, revenue_share_pct
from gold.kpi_top_sellers
order by revenue_decile;
