select payment_type, total_value, value_share_pct
from gold.kpi_payment_mix
order by total_value desc;
