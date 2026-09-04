WITH products AS (
    SELECT * FROM {{ref('bronze_products')}}
),
categories AS (
    SELECT * FROM {{ref('bronze_categories')}}
),
suppliers AS (
    SELECT * FROM {{ref('bronze_suppliers')}}
)
SELECT
    -- Primary and Foreign Key Columns
    CAST(p.product_id AS INTEGER) AS product_id,
    CAST(p.category_id AS INTEGER) AS category_id,
    CAST(p.supplier_id AS INTEGER) AS supplier_id,

    -- product details
    TRIM(p.product_name) AS product_name,
    TRIM(p.quantity_per_unit) AS quantity_per_unit,

    -- Categorie and Supplier details
    TRIM(c.category_name) AS category_name,
    TRIM(c.description) AS category_description,

    TRIM(s.company_name) AS supplier_name,
    TRIM(s.country) AS supplier_country,

    -- Prices and financial metrics
    CAST(COALESCE(p.unit_price, 0) AS DECIMAL(10, 2)) AS unit_price,
    CAST(COALESCE(p.units_in_stock, 0) AS INT) AS units_in_stock,
    CAST(COALESCE(p.units_on_order, 0) AS INT) AS units_on_order,
    CAST(COALESCE(p.reorder_level, 0) AS INT) AS reorder_level,

    -- Business Flags
    CASE
        WHEN p.discontinued = 1 THEN TRUE
        ELSE FALSE
    END AS is_discontinued,

    CASE
        WHEN p.units_in_stock = 0 THEN TRUE
        ELSE FALSE
    END AS is_out_of_stock,

    CASE
        WHEN COALESCE(p.units_in_stock, 0) + COALESCE(p.units_on_order, 0) <= COALESCE(p.reorder_level, 0) THEN TRUE
        ELSE FALSE
    END AS needs_reorder


FROM products p
LEFT JOIN categories c
ON p.category_id = c.category_id
LEFT JOIN suppliers s
ON p.supplier_id = s.supplier_id