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
    TRIM(c.address),
    TRIM(c.city),
    TRIM(c.country),

    -- Shipping address
    TRIM(o.ship_address),
    TRIM(o.ship_city),
    TRIM(o.ship_country),

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
    o.freight 

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id