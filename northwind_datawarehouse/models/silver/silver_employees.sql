WITH employees AS (
    SELECT * FROM {{ref('bronze_employees')}}
)
SELECT
    -- Employee Details
    e.employee_id,
    TRIM(e.last_name) AS last_name,
    TRIM(e.first_name) AS first_name,
    TRIM(e.title) AS title,
    CAST(e.birth_date AS DATE) AS birth_date,
    CAST(e.hire_date AS DATE) AS hire_date,
    TRIM(e.address) AS address,
    TRIM(e.city) AS city,
    TRIM(e.country) AS country,

    -- Manager Information
    CAST(e.reports_to AS INT) AS manager_id,
    TRIM(m.last_name) AS manager_last_name,
    TRIM(m.first_name) AS manager_first_name,
    TRIM(m.title) AS manager_title,

    -- Number of Direct Reports
    (SELECT COUNT(*) FROM employees WHERE reports_to = e.employee_id) AS num_direct_reports
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id