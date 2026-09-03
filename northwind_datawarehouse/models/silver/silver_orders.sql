WITH orders AS (
    SELECT * FROM {{ref('bronze_orders')}}
),
customers AS (
    SELECT * FROM {{ref('bronze_customers')}}
)
SELECT
    -- Primary and foreign keys
    o.order_id,
    o.customer_id,
    o.employee_id,

    -- Dates
    o.order_date,
    o.required_date,
    o.shipped_date,

    -- Customer address
    TRIM(c.address) AS customer_address,
    TRIM(c.city) AS customer_city,
    TRIM(c.country) AS customer_country,

    -- Shipping address
    TRIM(o.ship_address) AS ship_address,
    TRIM(o.ship_city) AS ship_city,
    TRIM(o.ship_country) AS ship_country,
    TRIM(o.ship_region) AS ship_region,

    -- Address comparison between customer and shipping addresses
    CASE
        WHEN TRIM(UPPER(c.address)) != TRIM(UPPER(o.ship_address))  THEN TRUE
        ELSE FALSE
    END AS is_different_shipping_address,

    -- Shipping status
    CASE
        WHEN o.shipped_date IS NULL THEN 'Pending'
        WHEN o.required_date < o.shipped_date THEN 'Delayed'
        ELSE 'On Time'
    END AS shipping_status,

    -- Freight cost
    o.freight AS freight

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id