WITH orders AS (
    SELECT * FROM {{ref('silver_orders')}}
),
orders_details AS (
    SELECT * FROM {{ref('silver_orders_details')}}
)
SELECT
    -- Surrogate key generation 
    {{dbt_utils.generate_surrogate_key(['o.order_id', 'od.product_id'])}} AS sales_id,
    o.order_id,
    od.product_id,
    o.customer_id,
    o.employee_id,
    o.order_date,
    o.required_date,
    o.shipped_date,
    o.is_different_shipping_address,
    o.shipping_status,
    o.freight,
    od.quantity_sold,
    od.actual_unit_price,
    od.catalog_unit_price,
    ROUND(od.discount_pct, 2) AS discount_pct,
    ROUND(od.net_revenue, 2) AS net_revenue,
    od.unit_price_diff,
    ROUND(od.revenue_impact, 2) AS revenue_impact,
    od.price_status

FROM orders o
JOIN orders_details od
    ON o.order_id = od.order_id