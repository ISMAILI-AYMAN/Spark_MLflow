select customer_state, order_count, customer_count, total_revenue, avg_order_value
from gold.kpi_regional_orders
order by total_revenue desc;
