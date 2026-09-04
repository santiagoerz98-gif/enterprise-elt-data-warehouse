WITH orders_details AS (
    SELECT * FROM {{ref('bronze_orders_details')}}
),
products AS (
    SELECT * FROM {{ref('bronze_products')}}
)
SELECT
    -- Primary and Foreign Key Columns
    CAST(od.order_id AS INTEGER) AS order_id,
    CAST(od.product_id AS INTEGER) AS product_id,

    -- Prices
    od.unit_price AS actual_unit_price,
    p.unit_price AS catalog_unit_price,
    CAST(od.quantity AS INTEGER) AS quantity_sold,
    od.discount AS discount_pct,

    -- Actual revenue
    (od.quantity * od.unit_price * (1-od.discount)) AS net_revenue,

    -- Price difference
    (od.unit_price - p.unit_price) AS unit_price_diff,

    -- Revenue impact of price difference
    (od.unit_price - p.unit_price) * od.quantity AS revenue_impact,
    
    -- Price status based on comparison with catalog price
    CASE 
        WHEN od.unit_price > p.unit_price THEN 'Above Catalog'
        WHEN od.unit_price < p.unit_price THEN 'Below Catalog'
        ELSE 'At Catalog'
    END AS price_status


FROM orders_details od
LEFT JOIN products p
ON od.product_id = p.product_id
