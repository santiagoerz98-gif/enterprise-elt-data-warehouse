WITH customers AS (
    SELECT * FROM {{ref('bronze_customers')}}
)
SELECT
    -- Primary key
    TRIM(customer_id) AS customer_id,

    -- Company information & contact
    COALESCE(TRIM(company_name), 'Unknown') AS company_name,
    COALESCE(TRIM(contact_name), 'Unknown') AS contact_name,
    COALESCE(TRIM(contact_title), 'Unknown') AS contact_title,

    -- Contact categorization
    CASE
        WHEN TRIM(LOWER(contact_title)) LIKE '%owner%' OR TRIM(LOWER(contact_title)) LIKE '%president%' THEN 'Executive'
        WHEN TRIM(LOWER(contact_title)) LIKE '%manager%' THEN 'Manager'
        WHEN TRIM(LOWER(contact_title)) LIKE '%sales%' OR TRIM(LOWER(contact_title)) LIKE '%representative%' THEN 'Sales'
        ELSE 'Other'
    END AS contact_role_category,

    -- Clean location information
    COALESCE(TRIM(address), 'N/A') AS customer_address,
    COALESCE(TRIM(city), 'N/A') AS city,
    COALESCE(TRIM(region), 'N/A') AS region,
    COALESCE(TRIM(postal_code), 'N/A') AS postal_code,
    COALESCE(TRIM(country), 'N/A') AS country,

    -- Customer market type ('Domestic' or 'International')
    CASE
        WHEN TRIM(LOWER(country)) = 'usa' THEN 'Domestic'
        ELSE 'International'
    END AS customer_market_type

FROM customers